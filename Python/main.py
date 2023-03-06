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


@app.route('/search', methods=['GET', 'POST'])
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
    cm_scores = cm.get_color_score("temp/" + image.filename)  # expects path to image
    # remove temp image
    os.remove("temp/" + image.filename)

    # get all image paths
    path_list = []
    for i, image in enumerate(os.listdir("/home/mortirreke/Desktop/assets/")):
        if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg"):
            path_list.append(image)

    path_list = set(path_list)

    results = []
    for path in path_list:
        pose_score = pd_scores.get(path, 0)
        object_score = od_scores.get(path, 0)
        color_score = cm_scores.get(path, 0)
        print(pose_score, object_score, color_score)

        weighted_score = pose_weight * pose_score + object_weight * object_score + color_weight * color_score
        # create dictionary of weighted score, pose score,object score, color score and path
        result = {"weighted_score": weighted_score, "pose_score": pose_score, "object_score": object_score,
                  "color_score": color_score, "image_name": os.path.basename(path)}
        results.append(result)
        results.sort(key=lambda x: x['weighted_score'], reverse=True)
        # print(results)
    return jsonify(results)


@app.route('/advancedSearch', methods=['GET', 'POST'])
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

import json
import pandas as pd
@app.route('/advancedSearchQuery', methods=['GET', 'POST'])
@cross_origin()
def advancedSearchQuery():
    image = request.files['image']
    object_weight = float(request.form['object_weight'])
    color_weight = float(request.form['color_weight'])
    pose_weight = float(request.form['pose_weight'])


    print("color weight: " + str(color_weight))
    print("object weight: " + str(object_weight))
    print("pose weight: " + str(pose_weight))


    objects = request.form['objects']
    poses = request.form['poses']
    colors = request.form['colors']

    # convert string to json
    objects = json.loads(objects)
    poses = json.loads(poses)
    colors = json.loads(colors)

    # convert the keypoints to pandas dataframe
    for pose in poses:
        pose['keypoints'] = pd.DataFrame.from_dict(pose['keypoints'], orient='index')

    pose_scores = pd.calculate_matches_improved(poses)
    objects_scores = od.get_object_scores(objects)
    colors_scores = cm.get_color_scores(colors)


    #loop over poses and filter out the ones that are not in the query (boolean is false)
    for pose in poses:
        if pose['bool'] == False:
            poses.remove(pose)

    print(poses)

if __name__ == '__main__':
    app.run()
