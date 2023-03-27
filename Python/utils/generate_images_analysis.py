from pose_matching import op_utils as op
from object_detection import od_utils as od
import os
import cv2


#loop through all images in the folder
path = "/home/mortirreke/Desktop/assets/"
for i,file in enumerate(os.listdir(path)):
    if file.endswith(".jpg"):
        #if image already exists in "/home/mortirreke/Desktop/assets/analysis/" skip it
        if os.path.isfile("/home/mortirreke/Desktop/assets/analysis/"+file):
            print("skipping "+file)
            continue
        #load image with opencv
        img = cv2.imread(path+file)
        poses = op.get_keypoints(img)
        print(poses)
        result_image, _ = od.get_objects(img)
        if poses:
            result_image = op.draw_poses(result_image, poses)
        #save image to "/home/mortirreke/Desktop/assets/analysis/"
        cv2.imwrite("/home/mortirreke/Desktop/assets/analysis/"+file, result_image)
