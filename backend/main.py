import base64
import os
import cv2
from pose_matching import op_utils as op
from object_detection import od_utils as od
from color_matching import cm_utils as cm
import numpy as np
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
import utils
app = Flask(__name__)
CORS(app)


@app.route('/precalcsearch', methods=['GET', 'POST'])
@cross_origin()
def precalc_search():
    pose_weight = float(request.form['pose_weight'])
    object_weight = float(request.form['object_weight'])
    color_weight = float(request.form['color_weight'])
    # check if the post request has the file part
    image_name = request.form['image_name']

    # display the image
    poses, pd_scores = op.get_precalc_pose_score(image_name)
    od_scores = od.get_precalc_scores(image_name)
    palette,cm_scores = cm.get_precalc_scores(image_name)

    # get all image paths
    with open('imagelist.pickle', 'rb') as handle:
        path_list = pickle.load(handle)

    path_list = set(path_list)

    all_colors = cm.load_data()

    result = {"results": []}
    for path in path_list:
        pose_score = pd_scores.get(path, 0)
        object_score = od_scores.get(path, 0)
        color_score = cm_scores.get(path, 0)

        weighted_score = pose_weight * pose_score + object_weight * object_score + color_weight * color_score
        # create dictionary of weighted score, pose score,object score, color score and path
        scores = {"weighted_score": weighted_score, "pose_score": pose_score, "object_score": object_score,
                  "color_score": color_score, "image_name": os.path.basename(path),
                  "metadata": utils.get_metadata(os.path.basename(path)), "palette": all_colors[path]}
        result["results"].append(scores)

    # load image from \precalculated_images
    result_image = cv2.imread("precalculated_images/" + image_name)
    # enode image as base64 to transfer to frontend
    _, img_encoded = cv2.imencode('.png', result_image)
    result_image = base64.b64encode(img_encoded).decode('utf-8')

    # add query image result to results
    result["queryImage"] = {"colorpalette": palette,
                            "result_image": result_image}

    result["results"].sort(key=lambda x: x['weighted_score'], reverse=True)
    # remove the first element, because it is the query image
    result["results"].pop(0)
    # get first 30 results
    result["results"] = result["results"][:60]
    # print(results)

    return jsonify(result)
@app.route('/search', methods=['GET', 'POST'])
@cross_origin()
def search():

    pose_weight = float(request.form['pose_weight'])
    object_weight = float(request.form['object_weight'])
    color_weight = float(request.form['color_weight'])
    #check if the post request has the file part


    image = request.files['image']

    # read the image file and convert to numpy array
    img_array = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    poses, pd_scores = op.get_pose_score2(img)
    result_image, od_scores = od.get_object_score(img)
    if poses:
        result_image = op.draw_poses(result_image, poses)

    image.stream.seek(0)
    image.save("temp/" + image.filename)
    palette, cm_scores = cm.get_color_score("temp/" + image.filename)  # expects path to image
    # remove temp image
    os.remove("temp/" + image.filename)


    # get all image paths
    with open('imagelist.pickle', 'rb') as handle:
        path_list = pickle.load(handle)

    path_list = set(path_list)

    result = {"results": []}
    for path in path_list:
        pose_score = pd_scores.get(path, 0)
        object_score = od_scores.get(path, 0)
        color_score = cm_scores.get(path, 0)

        weighted_score = pose_weight * pose_score + object_weight * object_score + color_weight * color_score
        # create dictionary of weighted score, pose score,object score, color score and path
        scores = {"weighted_score": weighted_score, "pose_score": pose_score, "object_score": object_score,
                  "color_score": color_score, "image_name": os.path.basename(path), "metadata" : utils.get_metadata(os.path.basename(path))}
        result["results"].append(scores)

    # enode image as base64 to transfer to frontend
    _, img_encoded = cv2.imencode('.png', result_image)
    result_image = base64.b64encode(img_encoded).decode('utf-8')

    #add query image result to results
    result["queryImage"] = {"colorpalette": palette,
    "result_image": result_image}

    result["results"].sort(key=lambda x: x['weighted_score'], reverse=True)
    # get first 30 results
    result["results"] = result["results"][:60]
    # print(results)


    return jsonify(result)


@app.route('/precalcadvancedSearch', methods=['GET', 'POST'])
@cross_origin()
def precalc_advancedSearch():
    image_name = request.form['image_name']

    analyse_pose = op.precalc_analyzePose(image_name)
    analyse_objects = od.precalc_analyze_objects(image_name)
    analyse_colors = cm.precalc_analyze_colors(image_name)

    result = {"type": "precalc" ,"image_name": image_name,"pose": analyse_pose, "objects": analyse_objects, "colors": analyse_colors}
    return jsonify(result)





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

    result = {"type": "custom", "pose": analyse_pose, "objects": analyse_objects, "colors": analyse_colors}
    return jsonify(result)


import json
import pandas as pd


@app.route('/advancedSearchQuery', methods=['GET', 'POST'])
@cross_origin()
def advancedSearchQuery():
    image = request.files['image']

    # read the image file and convert to numpy array
    img_array = np.frombuffer(image.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    object_weight = float(request.form['object_weight'])
    color_weight = float(request.form['color_weight'])
    pose_weight = float(request.form['pose_weight'])

    objects = request.form['objects']
    poses = request.form['poses']
    colors = request.form['colors']

    # convert string to json
    objects = json.loads(objects)
    poses = json.loads(poses)
    colors = json.loads(colors)

    ############## OBJECT MATCHING ################

    #filter out the objects that are not in the query (boolean is false)
    selected_objects = []
    for object in objects:
        if object['bool']:
            selected_objects.append(object['id'])

    object_scores = od.get_object_scores(selected_objects)
    object_image, _ = od.get_object_score(img)

    ############## POSE MATCHING ################

    # convert the keypoints to pandas dataframe
    for pose in poses:
        dataframe = pd.DataFrame.from_dict(pose['keypoints'], orient='index')
        sorted = dataframe.reindex(['Nose', 'Neck', 'RShoulder', 'RElbow', 'RWrist', 'LShoulder', 'LElbow', 'LWrist', 'MidHip', 'RHip', 'RKnee', 'RAnkle', 'LHip', 'LKnee', 'LAnkle', 'REye', 'LEye', 'REar', 'LEar', 'LBigToe', 'LSmallToe', 'LHeel', 'RBigToe', 'RSmallToe', 'RHeel'])
        pose['keypoints'] = sorted

    #loop over poses and filter out the ones that are not in the query (boolean is false)
    selected_poses = []
    for pose in poses:
        if pose['bool']:
            selected_poses.append(pose['keypoints'])

    pose_scores = op.calculate_matches_improved({"": selected_poses})
    result_image = op.draw_poses(object_image, {"": selected_poses})



    ############## COLOR MATCHING ################
    # filter out the colors that are not in the query (boolean is false)
    selected_colors = []
    for color in colors:
        if color['bool']:
            selected_colors.append(color['color'])

    color_scores = cm.get_color_scores(selected_colors)

    ############## WEIGHTED SCORES ################

    # get all image paths
    with open('imagelist.pickle', 'rb') as handle:
        path_list = pickle.load(handle)

    path_list = set(path_list)

    result = {"results": []}
    for path in path_list:
        pose_score = pose_scores.get(path, 0)
        object_score = object_scores.get(path, 0)
        color_score = color_scores.get(path, 0)

        weighted_score = pose_weight * pose_score + object_weight * object_score + color_weight * color_score

        # create dictionary of weighted score, pose score,object score, color score and path
        scores = {"weighted_score": weighted_score, "pose_score": pose_score, "object_score": object_score,
                  "color_score": color_score, "image_name": os.path.basename(path), "metadata" : utils.get_metadata(os.path.basename(path))}

        result["results"].append(scores)

    result["results"].sort(key=lambda x: x['weighted_score'], reverse=True)


    # enode image as base64 to transfer to frontend
    _, img_encoded = cv2.imencode('.png', result_image)
    result_image = base64.b64encode(img_encoded).decode('utf-8')

    result["queryImage"] = {"colorpalette": selected_colors,
                            "result_image": result_image}

    return jsonify(result)


@app.route('/precalcadvancedSearchQuery', methods=['GET', 'POST'])
@cross_origin()
def precalc_advancedSearchQuery():
    image_name = request.form['image_name']
    object_weight = float(request.form['object_weight'])
    color_weight = float(request.form['color_weight'])
    pose_weight = float(request.form['pose_weight'])

    objects = request.form['objects']
    poses = request.form['poses']
    colors = request.form['colors']

    # convert string to json
    objects = json.loads(objects)
    poses = json.loads(poses)
    colors = json.loads(colors)

    ############## OBJECT MATCHING ################

    #filter out the objects that are not in the query (boolean is false)
    selected_objects = []
    for object in objects:
        if object['bool']:
            selected_objects.append(object['id'])

    object_scores = od.get_object_scores(selected_objects)

    ############## POSE MATCHING ################

    # convert the keypoints to pandas dataframe
    for pose in poses:
        dataframe = pd.DataFrame.from_dict(pose['keypoints'], orient='index')
        sorted = dataframe.reindex(['Nose', 'Neck', 'RShoulder', 'RElbow', 'RWrist', 'LShoulder', 'LElbow', 'LWrist', 'MidHip', 'RHip', 'RKnee', 'RAnkle', 'LHip', 'LKnee', 'LAnkle', 'REye', 'LEye', 'REar', 'LEar', 'LBigToe', 'LSmallToe', 'LHeel', 'RBigToe', 'RSmallToe', 'RHeel'])
        pose['keypoints'] = sorted

    #loop over poses and filter out the ones that are not in the query (boolean is false)
    selected_poses = []
    for pose in poses:
        if pose['bool']:
            selected_poses.append(pose['keypoints'])

    pose_scores = op.calculate_matches_improved({"": selected_poses})


    ############## COLOR MATCHING ################
    # filter out the colors that are not in the query (boolean is false)
    selected_colors = []
    for color in colors:
        if color['bool']:
            selected_colors.append(color['color'])

    color_scores = cm.get_color_scores(selected_colors)

    ############## WEIGHTED SCORES ################

    # get all image paths
    with open('imagelist.pickle', 'rb') as handle:
        path_list = pickle.load(handle)

    path_list = set(path_list)

    result = {"results": []}
    for path in path_list:
        pose_score = pose_scores.get(path, 0)
        object_score = object_scores.get(path, 0)
        color_score = color_scores.get(path, 0)

        weighted_score = pose_weight * pose_score + object_weight * object_score + color_weight * color_score

        # create dictionary of weighted score, pose score,object score, color score and path
        scores = {"weighted_score": weighted_score, "pose_score": pose_score, "object_score": object_score,
                  "color_score": color_score, "image_name": os.path.basename(path), "metadata" : utils.get_metadata(os.path.basename(path))}

        result["results"].append(scores)

    result["results"].sort(key=lambda x: x['weighted_score'], reverse=True)
    #remove the first element, because it is the query image
    result["results"].pop(0)

    # load image from precalculated_images
    result_image = cv2.imread("precalculated_images/" + image_name)

    # enode image as base64 to transfer to frontend
    _, img_encoded = cv2.imencode('.png', result_image)
    result_image = base64.b64encode(img_encoded).decode('utf-8')

    result["queryImage"] = {"colorpalette": selected_colors,
                            "result_image": result_image}

    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3785)
