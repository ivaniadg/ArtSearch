from pose_matching import op_utils as op
from color_matching import cm_utils as cm
from object_detection import od_utils as od
import json
import pandas as pd
import utils
import pickle
import os


image_name = "andrea-del-sarto_archangel-raphael-with-tobias-st-lawrence-and-the-donor-leonardo-di-lorenzo-morelli-1512.jpg"


object_weight = 1
color_weight = 1
pose_weight = 1



objects = """
[{"bool": true, "id": 11, "label": "stop sign"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"},
 {"bool": true, "id": 0, "label": "person"}, {"bool": true, "id": 0, "label": "person"}]
"""
poses = """
[{"bool": true, "keypoints": {
    "LAnkle": {"x": 850, "y": 734}, "LBigToe": {"x": 825, "y": 738}, "LEar": {"x": 816, "y": 297},
    "LElbow": {"x": 791, "y": 428}, "LEye": {"x": 803, "y": 297}, "LHeel": {"x": 859, "y": 747},
    "LHip": {"x": 828, "y": 484}, "LKnee": {"x": 831, "y": 612}, "LShoulder": {"x": 819, "y": 347},
    "LSmallToe": {"x": 822, "y": 744}, "LWrist": {"x": 762, "y": 481}, "MidHip": {"x": 853, "y": 481},
    "Neck": {"x": 856, "y": 338}, "Nose": {"x": 797, "y": 309}, "RAnkle": {"x": 884, "y": 722},
    "RBigToe": {"x": 881, "y": 725}, "REar": {"x": 844, "y": 291}, "RElbow": {"x": 903, "y": 403},
    "REye": {"x": 0, "y": 0}, "RHeel": {"x": 887, "y": 734}, "RHip": {"x": 881, "y": 478},
    "RKnee": {"x": 869, "y": 606}, "RShoulder": {"x": 888, "y": 331}, "RSmallToe": {"x": 900, "y": 728},
    "RWrist": {"x": 0, "y": 0}}, "name": "Person1"}, {"bool": true, "keypoints": {"LAnkle": {"x": 472, "y": 694},
                                                                                  "LBigToe": {"x": 484, "y": 725},
                                                                                  "LEar": {"x": 0, "y": 0},
                                                                                  "LElbow": {"x": 516, "y": 391},
                                                                                  "LEye": {"x": 519, "y": 297},
                                                                                  "LHeel": {"x": 469, "y": 703},
                                                                                  "LHip": {"x": 487, "y": 453},
                                                                                  "LKnee": {"x": 491, "y": 578},
                                                                                  "LShoulder": {"x": 497, "y": 334},
                                                                                  "LSmallToe": {"x": 494, "y": 716},
                                                                                  "LWrist": {"x": 559, "y": 416},
                                                                                  "MidHip": {"x": 462, "y": 456},
                                                                                  "Neck": {"x": 469, "y": 328},
                                                                                  "Nose": {"x": 516, "y": 306},
                                                                                  "RAnkle": {"x": 412, "y": 647},
                                                                                  "RBigToe": {"x": 438, "y": 709},
                                                                                  "REar": {"x": 481, "y": 291},
                                                                                  "RElbow": {"x": 494, "y": 378},
                                                                                  "REye": {"x": 509, "y": 294},
                                                                                  "RHeel": {"x": 412, "y": 644},
                                                                                  "RHip": {"x": 437, "y": 456},
                                                                                  "RKnee": {"x": 444, "y": 562},
                                                                                  "RShoulder": {"x": 444, "y": 319},
                                                                                  "RSmallToe": {"x": 406, "y": 703},
                                                                                  "RWrist": {"x": 559, "y": 387}},
                                                      "name": "Person2"}, {"bool": true,
                                                                           "keypoints": {"LAnkle": {"x": 759, "y": 597},
                                                                                         "LBigToe": {"x": 763,
                                                                                                     "y": 606},
                                                                                         "LEar": {"x": 728, "y": 369},
                                                                                         "LElbow": {"x": 0, "y": 0},
                                                                                         "LEye": {"x": 713, "y": 369},
                                                                                         "LHeel": {"x": 759, "y": 597},
                                                                                         "LHip": {"x": 734, "y": 472},
                                                                                         "LKnee": {"x": 744, "y": 522},
                                                                                         "LShoulder": {"x": 741,
                                                                                                       "y": 397},
                                                                                         "LSmallToe": {"x": 0, "y": 0},
                                                                                         "LWrist": {"x": 0, "y": 0},
                                                                                         "MidHip": {"x": 716, "y": 472},
                                                                                         "Neck": {"x": 716, "y": 394},
                                                                                         "Nose": {"x": 709, "y": 375},
                                                                                         "RAnkle": {"x": 687, "y": 650},
                                                                                         "RBigToe": {"x": 675,
                                                                                                     "y": 669},
                                                                                         "REar": {"x": 697, "y": 372},
                                                                                         "RElbow": {"x": 688, "y": 437},
                                                                                         "REye": {"x": 703, "y": 369},
                                                                                         "RHeel": {"x": 694, "y": 659},
                                                                                         "RHip": {"x": 703, "y": 472},
                                                                                         "RKnee": {"x": 697, "y": 547},
                                                                                         "RShoulder": {"x": 694,
                                                                                                       "y": 394},
                                                                                         "RSmallToe": {"x": 678,
                                                                                                       "y": 669},
                                                                                         "RWrist": {"x": 691,
                                                                                                    "y": 481}},
                                                                           "name": "Person3"}, {"bool": true,
                                                                                                "keypoints": {
                                                                                                    "LAnkle": {"x": 650,
                                                                                                               "y": 744},
                                                                                                    "LBigToe": {"x": 0,
                                                                                                                "y": 0},
                                                                                                    "LEar": {"x": 594,
                                                                                                             "y": 469},
                                                                                                    "LElbow": {"x": 631,
                                                                                                               "y": 572},
                                                                                                    "LEye": {"x": 581,
                                                                                                             "y": 475},
                                                                                                    "LHeel": {"x": 672,
                                                                                                              "y": 750},
                                                                                                    "LHip": {"x": 647,
                                                                                                             "y": 631},
                                                                                                    "LKnee": {"x": 563,
                                                                                                              "y": 703},
                                                                                                    "LShoulder": {
                                                                                                        "x": 634,
                                                                                                        "y": 497},
                                                                                                    "LSmallToe": {
                                                                                                        "x": 0, "y": 0},
                                                                                                    "LWrist": {"x": 587,
                                                                                                               "y": 575},
                                                                                                    "MidHip": {"x": 634,
                                                                                                               "y": 631},
                                                                                                    "Neck": {"x": 612,
                                                                                                             "y": 503},
                                                                                                    "Nose": {"x": 575,
                                                                                                             "y": 487},
                                                                                                    "RAnkle": {"x": 647,
                                                                                                               "y": 734},
                                                                                                    "RBigToe": {"x": 0,
                                                                                                                "y": 0},
                                                                                                    "REar": {"x": 0,
                                                                                                             "y": 0},
                                                                                                    "RElbow": {"x": 581,
                                                                                                               "y": 575},
                                                                                                    "REye": {"x": 569,
                                                                                                             "y": 481},
                                                                                                    "RHeel": {"x": 675,
                                                                                                              "y": 738},
                                                                                                    "RHip": {"x": 619,
                                                                                                             "y": 634},
                                                                                                    "RKnee": {"x": 575,
                                                                                                              "y": 700},
                                                                                                    "RShoulder": {
                                                                                                        "x": 588,
                                                                                                        "y": 506},
                                                                                                    "RSmallToe": {
                                                                                                        "x": 0, "y": 0},
                                                                                                    "RWrist": {"x": 594,
                                                                                                               "y": 572}},
                                                                                                "name": "Person4"}, {
    "bool": true,
    "keypoints": {"LAnkle": {"x": 969, "y": 731}, "LBigToe": {"x": 0, "y": 0}, "LEar": {"x": 962, "y": 609},
                  "LElbow": {"x": 991, "y": 653}, "LEye": {"x": 959, "y": 609}, "LHeel": {"x": 0, "y": 0},
                  "LHip": {"x": 963, "y": 672}, "LKnee": {"x": 969, "y": 700}, "LShoulder": {"x": 963, "y": 631},
                  "LSmallToe": {"x": 0, "y": 0}, "LWrist": {"x": 0, "y": 0}, "MidHip": {"x": 959, "y": 675},
                  "Neck": {"x": 956, "y": 631}, "Nose": {"x": 959, "y": 612}, "RAnkle": {"x": 959, "y": 731},
                  "RBigToe": {"x": 0, "y": 0}, "REar": {"x": 956, "y": 612}, "RElbow": {"x": 938, "y": 647},
                  "REye": {"x": 959, "y": 609}, "RHeel": {"x": 956, "y": 738}, "RHip": {"x": 947, "y": 675},
                  "RKnee": {"x": 950, "y": 700}, "RShoulder": {"x": 944, "y": 631}, "RSmallToe": {"x": 0, "y": 0},
                  "RWrist": {"x": 941, "y": 653}}, "name": "Person5"}]
"""
colors = """
[
    {"bool": true, "color": [209, 184, 143]}, {"bool": true, "color": [109, 79, 47]}, {"bool": true,
                                                                                       "color": [144, 112, 77]}, {
        "bool": true, "color": [246, 237, 214]}, {"bool": true, "color": [109, 83, 68]}, {"bool": true,
                                                                                          "color": [107, 92, 69]}]
"""

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

all_colors = cm.load_data() # get all image paths
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
              "color_score": color_score, "image_name": os.path.basename(path), "metadata" : utils.get_metadata(os.path.basename(path)), "palette": all_colors[path]}

    result["results"].append(scores)



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
                  "color_score": color_score, "image_name": os.path.basename(path), "metadata" : utils.get_metadata(os.path.basename(path)), "palette": all_colors[path]}

        result["results"].append(scores)
