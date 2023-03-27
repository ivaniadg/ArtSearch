from object_detection import od_utils as od
# opencv
import cv2

#load image with opencv
img = cv2.imread("/home/mortirreke/Desktop/testpose.jpg")

_, matches = od.get_object_score(img)

min_value = min(matches.values())
max_value = max(matches.values())

print(min_value)
print(max_value)

# Plot all values in a histogram
import matplotlib.pyplot as plt
plt.hist(matches.values(), bins=20)
plt.show()

print(matches)