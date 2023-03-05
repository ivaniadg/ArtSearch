import cv2
import time
from pose_matching import op_utils as op
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.preprocessing import normalize
from skimage.transform import estimate_transform, warp

path= "/home/mortirreke/Desktop/test/two.jpg"
image1 = cv2.imread(path)

results = op.get_pose_score2(image1)

print(results)
#

# # image2 = cv2.imread("/home/mortirreke/Desktop/test/small.png")
#
# image_name = path.split("/")[-1]
#
# keypoints = op.get_keypoints(image1, image_name)
#
# print(keypoints)
#
# # print(df_array[0])
#
# score = op.similarity_score2(im1[0],im2[0])
#
# identical_score = op.similarity_score2(im1[0],im1[0])
#
# print("score: " + str(score))
# print("identical_score: " + str(identical_score))µ

#
#
# print("length 1: " + str(len(pose_dataframes)))
# poses = {}
# for df in pose_dataframes:
#     img_path = df.iloc[0]['path']
#     img_name = img_path.split("/")[-1]
#     #drop column path
#     df = df.drop(columns=['path'])
#     # check if image name is already in dictionary
#     if img_name in poses:
#         # if it is, append the new row
#         poses[img_name].append(df)
#     else:
#         # if it isn't, create a new key value pair
#         poses[img_name] = [df]
#
# import pickle
#
# with open('pose_matching/output/keypointsallnew.pickle', 'wb') as handle:
#     pickle.dump(poses, handle, protocol=pickle.HIGHEST_PROTOCOL)