from od_utils import *

# x = process_folder("/home/mortirreke/Desktop/assets/")
#
x = load_data()

# image = cv2.imread("/home/mortirreke/Desktop/assets/nicolas-poussin_holy-family-1650.jpg")
image = cv2.imread("/home/mortirreke/Desktop/poses/art26.jpg")
objs = get_objects(image)

result2 = find_matchesVec(objs, x, False)

print(result2[:10])

