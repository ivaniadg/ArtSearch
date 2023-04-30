from flask import Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_cors import CORS


# APP
app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']

# DB
db = SQLAlchemy(app)

# Task Broker
task_broker = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
task_broker.conf.update(app.config)
CORS(app)

from models import Actions, Top10

@app.route("/analytics", methods=["POST"])
def save_analytics():
    data = request.get_json()
    process_actions.apply_async(args=(data,))
    return make_response('Received', 200)


@task_broker.task(bind=True, name='process_actions')
def process_actions(self, data):
    for action in data:
        userID = action['userID']
        page = action['page']
        version = action['version']
        timestamp = action['timestamp']

        # extract the remaining fields from the action
        action.pop('userID', None)
        action.pop('page', None)
        action.pop('version', None)
        action.pop('timestamp', None)


        raw = Actions(userid=userID,
                      page=page,
                      version=version,
                      actions=action,
                      tstamp=timestamp)

        db.session.add(raw)
        db.session.commit()


# endpoint that takes top10 data and saves it to the database
@app.route("/analytics/top10", methods=["POST"])
def save_top10():
    data = request.get_json()
    process_top10.apply_async(args=(data,))
    return make_response('Received', 200)


@task_broker.task(bind=True, name='process_top10')
def process_top10(self, data):
    topX = data['topX']
    poseWeight = data['poseWeight']
    colorWeight = data['colorWeight']
    objectWeight = data['objectWeight']
    version = data['version']
    userID = data['userID']
    duration = data['secondsSpend']

    # Compute precision@k
    pak = precision_at_k(topX, k=6)

    src = spearman_correlation(topX)

    mserror = mse(topX)

    top10 = Top10(userid=userID,
                  version=version,
                  poseweight=poseWeight,
                  colorweight=colorWeight,
                  objectweight=objectWeight,
                  topX=topX,
                  pak=pak,
                  src=src,
                  mse=mserror,
                  duration=duration
                  )

    db.session.add(top10)
    db.session.commit()


def precision_at_k(images, k=6):
    """
    Calculates precision at k.

    Parameters:
    images (list): A list of dictionaries containing information about the images.
    k (int): The value of k for which precision is to be calculated.

    Returns:
    float: The precision at k.
    """
    if k <= 0:
        raise ValueError("k must be greater than zero.")

    num_correct = 0
    for i in range(k):
        print("index: " + str(i))
        print("images(i): "+ str(images[i]))
        if images[i]["personal_rank"] == images[i]["real_rank"]:
            num_correct += 1

    return num_correct / k


from scipy.stats import spearmanr


def spearman_correlation(image_list):
    """
    Computes the Spearman's rank correlation coefficient for a list of images.

    Args:
        image_list (list): A list of dictionaries representing images.

    Returns:
        float: Spearman's rank correlation coefficient.
    """

    # Get the list of personal ranks and real ranks
    personal_ranks = [x["personal_rank"] for x in image_list]
    real_ranks = [x["real_rank"] for x in image_list]

    # Compute Spearman's rank correlation coefficient
    correlation_coefficient, _ = spearmanr(personal_ranks, real_ranks)

    return correlation_coefficient


def mse(image_list):
    y_pred = [d["personal_rank"] for d in image_list]
    y_true = [d["real_rank"] for d in image_list]

    """
    Calculates the mean squared error (MSE).

    Parameters:
    y_true (list): A list of true values.
    y_pred (list): A list of predicted values.

    Returns:
    float: The MSE.
    """

    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")

    n = len(y_true)
    squared_errors = [(y_true[i] - y_pred[i]) ** 2 for i in range(n)]
    return sum(squared_errors) / n


# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=5000)
