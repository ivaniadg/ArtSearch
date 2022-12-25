# Some basic setup:
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
from scipy import spatial

setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random
import pickle

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
import os
from os import listdir

import copy

cfg = get_cfg()
# add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # set threshold for this model
# Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_X_101_32x8d_FPN_3x.yaml")
predictor = DefaultPredictor(cfg)


def get_label(number):
    dict = {0: u'__background__',
            1: u'person',
            2: u'bicycle',
            3: u'car',
            4: u'motorcycle',
            5: u'airplane',
            6: u'bus',
            7: u'train',
            8: u'truck',
            9: u'boat',
            10: u'traffic light',
            11: u'fire hydrant',
            12: u'stop sign',
            13: u'parking meter',
            14: u'bench',
            15: u'bird',
            16: u'cat',
            17: u'dog',
            18: u'horse',
            19: u'sheep',
            20: u'cow',
            21: u'elephant',
            22: u'bear',
            23: u'zebra',
            24: u'giraffe',
            25: u'backpack',
            26: u'umbrella',
            27: u'handbag',
            28: u'tie',
            29: u'suitcase',
            30: u'frisbee',
            31: u'skis',
            32: u'snowboard',
            33: u'sports ball',
            34: u'kite',
            35: u'baseball bat',
            36: u'baseball glove',
            37: u'skateboard',
            38: u'surfboard',
            39: u'tennis racket',
            40: u'bottle',
            41: u'wine glass',
            42: u'cup',
            43: u'fork',
            44: u'knife',
            45: u'spoon',
            46: u'bowl',
            47: u'banana',
            48: u'apple',
            49: u'sandwich',
            50: u'orange',
            51: u'broccoli',
            52: u'carrot',
            53: u'hot dog',
            54: u'pizza',
            55: u'donut',
            56: u'cake',
            57: u'chair',
            58: u'couch',
            59: u'potted plant',
            60: u'bed',
            61: u'dining table',
            62: u'toilet',
            63: u'tv',
            64: u'laptop',
            65: u'mouse',
            66: u'remote',
            67: u'keyboard',
            68: u'cell phone',
            69: u'microwave',
            70: u'oven',
            71: u'toaster',
            72: u'sink',
            73: u'refrigerator',
            74: u'book',
            75: u'clock',
            76: u'vase',
            77: u'scissors',
            78: u'teddy bear',
            79: u'hair drier',
            80: u'toothbrush'}
    return dict[number + 1]


def get_objects(image):
    outputs = predictor(image)
    objects = outputs["instances"].pred_classes.tolist()
    for o in objects:
        print("object detected: " + get_label(o))
    return objects


def generate_vector(list):
    vector = [0] * 80
    for x in list:
        vector[x] += 1

    return vector


def process_folder(path):
    list = []
    for i, image in enumerate(os.listdir(path)):
        # if i == 10:
        #     break
        print(i)
        if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg"):
            input = cv2.imread(path + image)
            list.append((get_objects(input), path + image))
    save_data(list)
    return list


def save_data(data):
    with open('object_detection/output/objects3.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_data():
    with open('object_detection/output/objects3.pickle', 'rb') as handle:
        return pickle.load(handle)


def get_score(list1,list2):
    score = 0
    inputcopy = copy.copy(list1)
    for object2 in list2:
        for object1 in inputcopy:
            if object1 == object2:
                inputcopy.remove(object1)
                score = score + 1
    return score


def find_matches(input, data):
    scores = []
    for image in data:
        objects = image[0]
        score = 0
        inputcopy = copy.copy(input)
        for object2 in objects:
            for object1 in inputcopy:
                if object1 == object2:
                    inputcopy.remove(object1)
                    score = score + 1
        scores.append((image[1], score))
    return scores


def find_matchesVec(input, data, detect_persons=True):
    max = 0.001
    scores = []
    for image in data:
        objects = image[0]
        vec1 = generate_vector(objects)
        vec2 = generate_vector(input)
        if not detect_persons:
            vec1.pop(0)
            vec2.pop(0)
        nv1 = normalize(vec1)
        nv2 = normalize(vec2)
        score = spatial.distance.euclidean(nv1, nv2)
        if score > max:
            max = score
        scores.append((score,image[1]))

    normalized = adjustRange(max, scores)
    sorted_res = sorted(normalized, key=lambda tup: tup[0], reverse=True)
    return sorted_res

def adjustRange(max, scores) -> list:
    for i,score in enumerate(scores):
        scores[i] = (1-score[0]/max,score[1])
    return scores

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def od_get_scores(imagepath) -> list:
    x = load_data()
    image = cv2.imread(imagepath)
    objs = get_objects(image)
    return find_matchesVec(objs, x, False)