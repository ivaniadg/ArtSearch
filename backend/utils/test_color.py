from color_matching import cm_utils as cm
# opencv
import cv2

# _, matches = cm.get_color_score("/home/mortirreke/Desktop/assets/aleksandra-ekster_costume-design-for-salome-1917.jpg")
#
# min_value = min(matches.values())
# max_value = max(matches.values())
#
# print(min_value)
# print(max_value)
#
# # Plot all values in a histogram
# import matplotlib.pyplot as plt
# plt.hist(matches.values(), bins=20)
# plt.show()
#
# print(matches)

x = cm.load_data()
print(x)