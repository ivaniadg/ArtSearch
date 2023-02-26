import cv2
import time
from op_utils import *

# cam = cv2.VideoCapture(0)
# # time.sleep(3)
# result, image = cam.read()

image = cv2.imread("/home/mortirreke/Desktop/assets/nicolas-poussin_holy-family-1650.jpg")

df_array = get_keypoints(image)

image = drawKeypoints(df_array[0], show_image=True, image=image)


similarity_scores = find_best_match(df_array[0])

print(similarity_scores)

# for result in similarity_scores:
#     pose2 = result[1]
#
#     im1 = drawKeypoints(df_array[0], show_image=True, image=image)
#     im2 = drawKeypoints(pose2,show_image=True)
#
#     im2 = cv2.putText(im2, str(result[0]), (0,30), cv2.FONT_HERSHEY_SIMPLEX,
#                    1, (0,0,255), 1, 2)
#
#     cv2.imshow("image1",image)
#     cv2.imshow("image2",im2)
#     key = cv2.waitKey(0)
#     if key == 27: break
#
#     cv2.destroyAllWindows()
# cv2.destroyAllWindows()


