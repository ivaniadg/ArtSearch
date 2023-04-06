import sys
import cv2
import numpy as np
import argparse
import pandas as pd
import math
import copy
import time
import pickle
from itertools import zip_longest
from scipy import spatial
import matplotlib.pyplot as plt

sys.path.append("/usr/local/python")
from openpose import pyopenpose as op
import base64
import os
from sklearn.preprocessing import normalize


def get_keypoints(image, image_name="") -> dict:
    # Flags
    parser = argparse.ArgumentParser()
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "pose_matching/models/"
    params["net_resolution"] = "320x320"

    BODY_PARTS = op.getPoseBodyPartMapping(op.BODY_25)

    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1]) - 1:
            next_item = args[1][i + 1]
        else:
            next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-', '')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-', '')
            if key not in params: params[key] = next_item

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    datum = op.Datum()
    datum.cvInputData = image
    opWrapper.emplaceAndPop(op.VectorDatum([datum]))
    network_output = datum.poseKeypoints

    # Unwrapping Person Keypoints from Openpose Network Output

    keypoints = {}
    index_names = copy.deepcopy(BODY_PARTS)
    index_names.pop(25)
    if network_output is not None:
        poses = []
        for human in network_output:
            output_sub_arr = {}
            for i in range(len(human)):
                output_sub_arr[BODY_PARTS[i]] = [int(human[i][0]), int(human[i][1])]
            # print("\n   Person Detected")
            # print(output_sub_arr)

            poses.append(pd.DataFrame(output_sub_arr.values(), columns=['x', 'y'], index=list(index_names.values())))
        keypoints[image_name] = poses
    # else:
    #     print("no keypoints detected for :" + image)
    #     # return None;

    return keypoints


from scipy.spatial import procrustes

from skimage.transform import estimate_transform, warp
from scipy.spatial.distance import euclidean


## This function is used to calculate the similarity percentage between two poses on how good they match, regardless on their position in the picture.
def similarity_score2(pose1: pd.DataFrame, pose2: pd.DataFrame) -> float:
    """
    This function is used to calculate the similarity percentage between two poses on how good they match, regardless on their position in the picture.

    Args:
    pose1 (pd.DataFrame): dataframe containing the X and Y coordinates of keypoints, and imagepath for the first pose
    pose2 (pd.DataFrame): dataframe containing the X and Y coordinates of keypoints for the second pose

    Returns:
    score (float): similarity percentage between the two poses
    """

    # Extract keypoint coordinates from the dataframes
    keypoints1 = pose1[['x', 'y']].astype(float).values
    keypoints2 = pose2[['x', 'y']].astype(float).values

    # Normalize the keypoints to have unit norm
    norm1 = np.linalg.norm(keypoints1)
    norm2 = np.linalg.norm(keypoints2)
    keypoints1 /= norm1
    keypoints2 /= norm2

    # Compute the Procrustes transformation between the normalized poses
    mtx1, mtx2, disparity = procrustes(keypoints1, keypoints2)

    # Calculate the similarity score based on the sum of squared differences between corresponding keypoints
    ssd = np.sum((mtx1 - mtx2) ** 2)
    max_ssd = np.sum(keypoints1 ** 2) + np.sum(keypoints2 ** 2)
    similarity = 1 - (ssd / max_ssd)

    return similarity


def similarity_score(pose1: pd.DataFrame, pose2: pd.DataFrame):
    p1 = []
    p2 = []
    # Remove keypoints when keypoint values is none
    pose1_df = pd.DataFrame(pose1, columns=['x', 'y'])
    pose2_df = pd.DataFrame(pose2, columns=['x', 'y'])
    # pose_df = pd.concat([pose1, pose2],axis = 1).dropna().reset_index(drop=True)
    # pose1_df = pose1.rename({'x':})
    # pose2_df = pose_df[['Xp2','Yp2']]

    pose1 = pose1_df.to_numpy()
    pose2 = pose2_df.to_numpy()

    pose_1 = np.array(pose1, dtype=float)
    pose_2 = np.array(pose2, dtype=float)

    # Normalize coordinates
    pose_1[:, 0] = pose_1[:, 0] / max(pose_1[:, 0])
    pose_1[:, 1] = pose_1[:, 1] / max(pose_1[:, 1])
    pose_2[:, 0] = pose_2[:, 0] / max(pose_2[:, 0])
    pose_2[:, 1] = pose_2[:, 1] / max(pose_2[:, 1])

    # Turn (16x2) into (32x1)
    for joint in range(pose_1.shape[0]):
        x1 = pose_1[joint][0]
        y1 = pose_1[joint][1]
        x2 = pose_2[joint][0]
        y2 = pose_2[joint][1]

        p1.append(x1)
        p1.append(y1)
        p2.append(x2)
        p2.append(y2)

    p1 = np.array(p1)
    p2 = np.array(p2)

    # Looking to minimize the distance if there is a match
    # Computing two different distance metrics
    cosineDistance = spatial.distance.cosine(p1, p2)
    euclideanDistance = math.sqrt(2 * cosineDistance)

    return 1 - cosineDistance

def draw_poses(image, poses):
    poses = poses.get('', [])
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (255, 255, 255), (0, 0, 0)]
    for i, pose in enumerate(poses):
        #if i is greater than the number of colors, reset to 0
        if i >= len(colors):
            i = 0
        image = drawKeypoints(pose, show_image=True, image=image, color=colors[i])
    return image

def analyzePose(image):
    poselist = get_keypoints(image)
    #extract poses from dictionary
    poses = poselist.get('', [])

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (255, 255, 255), (0, 0, 0)]

    #check if poses is empty
    if not poses:
        # enode image as base64 to transfer to frontend
        _, img_encoded = cv2.imencode('.png', image)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        return {"image": img_base64, "persons": []}

    for i, pose in enumerate(poses):
        image = drawKeypoints(pose, show_image=True, image=image, color=colors[i])
    # enode image as base64 to transfer to frontend
    _, img_encoded = cv2.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
    # create person strings
    persons = []
    for i, pose in enumerate(poses):
        #convert pose (pandas dataframe) to list of dictionaries
        pose = pose.to_dict('index')
        persons.append({"name": "Person" + str(i + 1), "bool": True, "keypoints": pose})

    return {"image": img_base64, "persons": persons}


def precalc_analyzePose(image_name):
    poses = get_all_keypoints()
    poses = poses.get(image_name, [])

    #load image from precalculated_images
    image = cv2.imread("precalculated_images/" + image_name)

    # enode image as base64 to transfer to frontend
    _, img_encoded = cv2.imencode('.png', image)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
    # create person strings
    persons = []
    for i, pose in enumerate(poses):
        #convert pose (pandas dataframe) to list of dictionaries
        pose = pose.to_dict('index')
        persons.append({"name": "Person" + str(i + 1), "bool": True, "keypoints": pose})

    return {"image": img_base64, "persons": persons}


def drawKeypoints(pose1: pd.DataFrame, show_image=False, size=512, image=[], color=(0, 0, 255)):
    if show_image:
        canvas = image
    else:
        # canvas =  np.ones(shape=(size,size,3), dtype=np.int16)
        canvas = np.zeros([size, size, 3])

    nose = (pose1.loc["Nose"]['x'], pose1.loc["Nose"]['y'])
    neck = (pose1.loc["Neck"]['x'], pose1.loc["Neck"]['y'])
    RShoulder = (pose1.loc["RShoulder"]['x'], pose1.loc["RShoulder"]['y'])
    RElbow = (pose1.loc["RElbow"]['x'], pose1.loc["RElbow"]['y'])
    RWrist = (pose1.loc["RWrist"]['x'], pose1.loc["RWrist"]['y'])
    LShoulder = (pose1.loc["LShoulder"]['x'], pose1.loc["LShoulder"]['y'])
    LElbow = (pose1.loc["LElbow"]['x'], pose1.loc["LElbow"]['y'])
    LWrist = (pose1.loc["LWrist"]['x'], pose1.loc["LWrist"]['y'])
    MidHip = (pose1.loc["MidHip"]['x'], pose1.loc["MidHip"]['y'])
    RHip = (pose1.loc["RHip"]['x'], pose1.loc["RHip"]['y'])
    RKnee = (pose1.loc["RKnee"]['x'], pose1.loc["RKnee"]['y'])
    RAnkle = (pose1.loc["RAnkle"]['x'], pose1.loc["RAnkle"]['y'])
    LHip = (pose1.loc["LHip"]['x'], pose1.loc["LHip"]['y'])
    LKnee = (pose1.loc["LKnee"]['x'], pose1.loc["LKnee"]['y'])
    LAnkle = (pose1.loc["LAnkle"]['x'], pose1.loc["LAnkle"]['y'])
    REye = (pose1.loc["REye"]['x'], pose1.loc["REye"]['y'])
    LEye = (pose1.loc["LEye"]['x'], pose1.loc["LEye"]['y'])
    REar = (pose1.loc["REar"]['x'], pose1.loc["REar"]['y'])
    LEar = (pose1.loc["LEar"]['x'], pose1.loc["LEar"]['y'])
    LBigToe = (pose1.loc["LBigToe"]['x'], pose1.loc["LBigToe"]['y'])
    LSmallToe = (pose1.loc["LSmallToe"]['x'], pose1.loc["LSmallToe"]['y'])
    LHeel = (pose1.loc["LHeel"]['x'], pose1.loc["LHeel"]['y'])
    RBigToe = (pose1.loc["RBigToe"]['x'], pose1.loc["RBigToe"]['y'])
    RSmallToe = (pose1.loc["RSmallToe"]['x'], pose1.loc["RSmallToe"]['y'])
    RHeel = (pose1.loc["RHeel"]['x'], pose1.loc["RHeel"]['y'])

    if nose != (0, 0) and neck != (0, 0):
        cv2.line(canvas, nose, neck, color, 3)
    if REye != (0, 0) and nose != (0, 0):
        cv2.line(canvas, nose, REye, color, 3)
    if REye != (0, 0) and REar != (0, 0):
        cv2.line(canvas, REar, REye, color, 3)

    if LEye != (0, 0) and nose != (0, 0):
        cv2.line(canvas, nose, LEye, color, 3)
    if LEye != (0, 0) and LEar != (0, 0):
        cv2.line(canvas, LEar, LEye, color, 3)

    # spine
    if MidHip != (0, 0) and neck != (0, 0):
        cv2.line(canvas, MidHip, neck, color, 3)
    if MidHip != (0, 0) and RHip != (0, 0):
        cv2.line(canvas, MidHip, RHip, color, 3)
    if MidHip != (0, 0) and LHip != (0, 0):
        cv2.line(canvas, MidHip, LHip, color, 3)

    # Right hand
    if RShoulder != (0, 0) and neck != (0, 0):
        cv2.line(canvas, RShoulder, neck, color, 3)
    if RElbow != (0, 0) and RShoulder != (0, 0):
        cv2.line(canvas, RShoulder, RElbow, color, 3)
    if RWrist != (0, 0) and RElbow != (0, 0):
        cv2.line(canvas, RWrist, RElbow, color, 3)

    # Left arm
    if neck != (0, 0) and LShoulder != (0, 0):
        cv2.line(canvas, LShoulder, neck, color, 3)
    if LElbow != (0, 0) and LShoulder != (0, 0):
        cv2.line(canvas, LShoulder, LElbow, color, 3)
    if LWrist != (0, 0) and LElbow != (0, 0):
        cv2.line(canvas, LWrist, LElbow, color, 3)

    # Left leg
    if LKnee != (0, 0) and LHip != (0, 0):
        cv2.line(canvas, LKnee, LHip, color, 3)
    if LKnee != (0, 0) and LAnkle != (0, 0):
        cv2.line(canvas, LKnee, LAnkle, color, 3)
    if LAnkle != (0, 0) and LHeel != (0, 0):
        cv2.line(canvas, LHeel, LAnkle, color, 3)
    if LAnkle != (0, 0) and LHeel != (0, 0):
        cv2.line(canvas, LBigToe, LAnkle, color, 3)
    if LAnkle != (0, 0) and LHeel != (0, 0):
        cv2.line(canvas, LBigToe, LAnkle, color, 3)
    if LSmallToe != (0, 0) and LBigToe != (0, 0):
        cv2.line(canvas, LBigToe, LSmallToe, color, 3)

    # Right leg
    if RKnee != (0, 0) and RHip != (0, 0):
        cv2.line(canvas, RKnee, RHip, color, 3)
    if RKnee != (0, 0) and RAnkle != (0, 0):
        cv2.line(canvas, RKnee, RAnkle, color, 3)
    if RAnkle != (0, 0) and RHeel != (0, 0):
        cv2.line(canvas, RHeel, RAnkle, color, 3)
    if RAnkle != (0, 0) and RHeel != (0, 0):
        cv2.line(canvas, RBigToe, RAnkle, color, 3)
    if RAnkle != (0, 0) and RHeel != (0, 0):
        cv2.line(canvas, RBigToe, RAnkle, color, 3)
    if RSmallToe != (0, 0) and RBigToe != (0, 0):
        cv2.line(canvas, RBigToe, RSmallToe, color, 3)

    return canvas


# def find_best_match(pose1):
#     #load all keypoints
#     with open('pose_matching/output/keypointsall.pickle', 'rb') as handle:
#         poses = pickle.load(handle)
#
#     # Calculate every score
#     similarity_scores = []
#     for pose2 in poses:
#         score = similarity_score(pose1, pose2)
#         similarity_scores.append((score, pose2.iloc[0].path))
#     similarity_scores.sort(key=lambda tup: tup[0], reverse=True)
#     return similarity_scores


# def find_best_match(pose_list):
#     #load all keypoints
#     with open('pose_matching/output/keypointsall.pickle', 'rb') as handle:
#         all_poses = pickle.load(handle)
#
#     # Calculate every score
#     similarity_scores = []
#     for pose1 in all_poses:
#         score = 0
#         for pose2 in pose_list:
#             score += similarity_score(pose1, pose2)
#         similarity_scores.append((score, pose1.iloc[0].path))
#     return similarity_scores

def get_all_keypoints():
    file_path = os.path.join(os.path.dirname(__file__), 'output', 'keypointsallnew.pickle')

    # load all keypoints
    with open(file_path, 'rb') as handle:
        poses = pickle.load(handle)
    return poses


## Method 1: Calculate the similarity score between two poses. loops through all the poses and takes the best score for each pose. this is the score for the image
def calculate_matches(query_poses):
    images = get_all_keypoints()  # Get keypoints (dictionary) for all poses in all pictures

    # print(images)
    similarity_scores = {}  # Keep track of the similarity scores for each image

    for query_pose in query_poses:
        for image_name, poses in images.items():
            best_score = float('-inf')
            # Calculate the similarity score between the query pose and each pose in the image
            for pose in poses:
                score = similarity_score2(query_pose, pose)
                # Keep track of the best score for this image
                if score > best_score:
                    best_score = score
            # Store the best score for this image
            similarity_scores[image_name] = best_score

    # covert to list
    similarity_scores = [(v, k) for k, v in similarity_scores.items()]
    return similarity_scores

def calculate_matches_improved(query_poses: dict):
    query_poses = query_poses.get("", [])
    if not query_poses:
        return {}

    images = get_all_keypoints()  # Get keypoints (dictionary) for all poses in all pictures

    similarity_scores = []  # Keep track of the similarity scores for each image

    for query_pose in query_poses:
        for image_name, poses in images.items():
            best_score = float('-inf')
            # Calculate the similarity score between the query pose and each pose in the image
            for pose in poses:

                score = similarity_score2(query_pose, pose)
                # Keep track of the best score for this image
                if score > best_score:
                    best_score = score
            # Store the best score for this image
            similarity_scores.append((best_score, image_name))

    summed_scores = {}
    for score, image_name in similarity_scores:
        if image_name in summed_scores:
            summed_scores[image_name] += score
        else:
            summed_scores[image_name] = score

    # normalize between 0 and 1
    max_score = max(summed_scores.values())
    min_score = min(summed_scores.values())
    for image_name, score in summed_scores.items():
        summed_scores[image_name] = (score - min_score) / (max_score - min_score)

    return summed_scores

def get_pose_score(image):
    df_array = get_keypoints(image)
    if not df_array:
        return 0
    else:
        return calculate_matches(df_array)


def get_pose_score2(image):
    poses = get_keypoints(image)
    if not poses:
        return None, {}
    else:
        return poses, calculate_matches_improved(poses)

def get_precalc_pose_score(image_name):
    poses = get_all_keypoints()
    poses = poses.get(image_name, [])
    if not poses:
        return None, {}
    else:
        return poses, calculate_matches_improved({"":poses})
