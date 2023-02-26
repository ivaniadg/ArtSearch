import os

import cv2

from pose_matching import op_utils as op
from object_detection import od_utils as od
from color_matching import cm_utils as cm

import flask


path = "/home/mortirreke/Desktop/assets/"
image = "images_594.jpg"

image_path = path+image



pose_weight = 1
object_weight = 0
color_weight = 0

pd_scores = op.pd_get_scores(image_path)
od_scores = od.od_get_scores(image_path)
cm_scores = cm.cm_get_scores(image_path)


print(cm_scores)


def recalc_scores(pd_scores, od_scores,cm_scores ,pd_weight, od_weight,cm_weight):
    path_list = []
    for i, image in enumerate(os.listdir("/home/mortirreke/Desktop/assets/")):
        if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg"):
            path_list.append("/home/mortirreke/Desktop/assets/" + image)

    weighted_scores = []
    for path in path_list:
        pose_score = 0
        object_score = 0
        color_score = 0
        for pd_score in pd_scores:
            if pd_score[1] == path:
                pose_score = pd_score[0]
        for od_score in od_scores:
            if od_score[1] == path:
                object_score = od_score[0]
        for cm_score in cm_scores:
            if cm_score[1] == path:
                color_score = cm_score[0]
        weighted_score = pd_weight * pose_score + od_weight * object_score + cm_weight * color_score
        weighted_scores.append((weighted_score, path))
    return weighted_scores

# flask api end poin

res = recalc_scores(pd_scores,od_scores,cm_scores, pose_weight,object_weight,color_weight)

x = sorted(res, key=lambda tup: tup[0], reverse=True)

print(x)
#function that takes in the scores and path and shows the top 5 images
def show_results(res):
    for i in range(5):
        print(res[i][1])
        image = cv2.imread(res[i][1])
        cv2.imshow("image", image)
        cv2.waitKey(0)

show_results(x)