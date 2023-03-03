import cv2
import time
from pose_matching import op_utils as op
import pandas as pd
import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.preprocessing import normalize
from skimage.transform import estimate_transform, warp


image1 = cv2.imread("/home/mortirreke/Desktop/test/large.jpg")
image2 = cv2.imread("/home/mortirreke/Desktop/test/small.png")

im1 = op.get_keypoints(image1)
im2 = op.get_keypoints(image2)


# print(df_array[0])

score = op.similarity_score2(im1[0],im2[0])

identical_score = op.similarity_score2(im1[0],im1[0])

print("score: " + str(score))
print("identical_score: " + str(identical_score))

