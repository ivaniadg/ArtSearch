import os
import cv2
from pose_matching import op_utils as op
from object_detection import od_utils as od
from color_matching import cm_utils as cm
import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['GET','POST'])
@cross_origin()
def search():
    pose_weight = float(request.form['pose_weight'])
    object_weight = float(request.form['object_weight'])
    color_weight = float(request.form['color_weight'])
    image = request.files['image']

    # read the image file and convert to numpy array
    img_array = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    pd_scores = op.get_pose_score2(img)
    od_scores = od.get_object_score(img)
    image.stream.seek(0)
    image.save("temp/" + image.filename)
    cm_scores = cm.get_color_score("temp/" + image.filename) #expects path to image
    # remove temp image
    os.remove("temp/" + image.filename)


    # get all image paths
    path_list = []
    for i, image in enumerate(os.listdir("/home/mortirreke/Desktop/assets/")):
        if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg"):
            path_list.append("/home/mortirreke/Desktop/assets/" + image)

    results = []
    for path in path_list:
        pose_score = 0
        object_score = 0
        color_score = 0
        if pd_scores == None:
            pd_scores = []
        for pd_score in pd_scores:
            if pd_score[1] == path:
                pose_score = pd_score[0]
        for od_score in od_scores:
            if od_score[1] == path:
                object_score = od_score[0]
        for cm_score in cm_scores:
            if cm_score[1] == path:
                color_score = cm_score[0]
        weighted_score = pose_weight * pose_score + object_weight * object_score + color_weight * color_score
        #create dictionary of weighted score, pose score,object score, color score and path
        result = {"weighted_score": weighted_score, "pose_score": pose_score, "object_score": object_score, "color_score": color_score, "image_name": os.path.basename(path)}
        results.append(result)
        results.sort(key=lambda x: x['weighted_score'], reverse=True)
    return jsonify(results)


@app.route('/advancedSearch', methods=['GET','POST'])
@cross_origin()
def advancedSearch():
    image = request.files['image']
    # read the image file and convert to numpy array
    img_array = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    analyse_pose = op.analyzePose(img)
    analyse_objects = od.analyze_objects(img)
    image.stream.seek(0)
    image.save("temp/" + image.filename)
    analyse_colors = cm.analyze_colors("temp/" + image.filename)
    # remove temp image
    os.remove("temp/" + image.filename)

    result = {"pose": analyse_pose, "objects": analyse_objects, "colors": analyse_colors}
    return jsonify(result)

if __name__ == '__main__':
    app.run()