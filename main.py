import os

from pose_matching import op_utils as op
from object_detection import od_utils as od

path = "/home/mortirreke/Desktop/assets/"
image = "james-mcneill-whistler_the-japanese-dress-1890.jpg"

image_path = path+image



pose_weight = 1
object_weight = 1-pose_weight

pd_scores = op.pd_get_scores(image_path)
od_scores = od.od_get_scores(image_path)

# print(pd_scores[0][0])



# print(pd_scores[:5])
# print(od_scores[:5])


def recalc_scores(pd_scores, od_scores, pd_weight, od_weight):
    path_list = []
    for i, image in enumerate(os.listdir("/home/mortirreke/Desktop/assets/")):
        if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg"):
            path_list.append("/home/mortirreke/Desktop/assets/" + image)

    weighted_scores = []
    for path in path_list:
        pose_score = 0
        object_score = 0
        for pd_score in pd_scores:
            if pd_score[1] == path:
                pose_score = pd_score[0]
        for od_score in od_scores:
            if od_score[1] == path:
                object_score = od_score[0]
        weighted_score = pd_weight * pose_score + od_weight * object_score

        weighted_scores.append((weighted_score, path))
    return weighted_scores


res = recalc_scores(pd_scores,od_scores, pose_weight,object_weight)

x = sorted(res, key=lambda tup: tup[0], reverse=True)

print(x)