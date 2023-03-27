from pose_matching import op_utils as op
# opencv
import cv2

#load image with opencv
img = cv2.imread("/home/mortirreke/Desktop/assets/antoine-watteau_the-flautist.jpg")

_, matches = op.get_pose_score2(img)

min_value = min(matches.values())
max_value = max(matches.values())

print(min_value)
print(max_value)

# Plot all values in a histogram
import matplotlib.pyplot as plt
plt.hist(matches.values(), bins=20)
plt.show()

print(matches)