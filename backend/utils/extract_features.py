from pose_matching import op_utils as op
from color_matching import cm_utils as cm
from object_detection import od_utils as od
import os
import cv2
from colorthief import ColorThief
import pickle


def extract_features(folder):
    # initialize the index dictionary to store the image name
    # and corresponding histograms and the images dictionary
    # to store the images themselves
    index = {}

    colors_dict = {}
    objects_dict = {}
    poses_dict = {}

    for i, image_name in enumerate(os.listdir(folder)):
        if image_name.endswith(".png") or image_name.endswith(".jpg") or image_name.endswith(".jpeg"):
            # print progress
            print("Processing image " + str(i) + " of " + str(len(os.listdir(folder))))
            if i == 5:
                break
            image = cv2.imread(folder + image_name)

            #display image
            keypoints = op.get_keypoints(image)
            poses_dict[image_name] = keypoints

            color_thief = ColorThief(folder + image_name)
            palette = color_thief.get_palette(color_count=6)
            colors_dict[image_name] = palette

            result_image, objects = od.get_objects(image)
            objects = od.generate_vector(objects)
            objects_dict[image_name] = objects

            result_image = op.draw_poses(result_image, keypoints)

            cv2.imwrite(folder + "analysis/" + image_name, result_image)

    cm.save_data(colors_dict)
    od.save_data(objects_dict)
    op.save_data(poses_dict)
    return index

#adds an image to the already existing index
def add_image(image_path):

    image_name = image_path.split("/")[-1]

    all_keypoints = op.get_all_keypoints()
    all_colors = cm.load_data()
    all_objects = od.load_data()

    image = cv2.imread(image_path)

    keypoints = op.get_keypoints(image)

    color_thief = ColorThief(image_path)
    palette = color_thief.get_palette(color_count=6)

    result_image, objects = od.get_objects(image)
    # objects = od.generate_vector(objects)

    result_image = op.draw_poses(result_image, keypoints)

    cv2.imwrite("/home/mortirreke/Desktop/"+image_name , result_image)

    all_keypoints[image_name] = keypoints['']
    all_colors[image_name] = palette
    all_objects[image_name] = objects

    with open('../imagelist.pickle', 'rb') as handle:
        path_list = pickle.load(handle)

    path_list.append(image_name)

    with open('../imagelist.pickle', 'wb') as handle:
        pickle.dump(path_list, handle, protocol=pickle.HIGHEST_PROTOCOL)


    cm.save_data(all_colors)
    od.save_data(all_objects)
    op.save_data(all_keypoints)


# extract_features("/home/mortirreke/Desktop/assets/")

add_image("/home/mortirreke/Pictures/good/L-Davinci_Mona-lisa.jpg")
add_image("/home/mortirreke/Pictures/good/Margritte_son-of-man.jpg")
add_image("/home/mortirreke/Pictures/good/Jean-Beraud_Au-Café.jpg")
add_image("/home/mortirreke/Pictures/good/Diego-Rivera_Self-portrait.jpg")
add_image("/home/mortirreke/Pictures/good/unknown_unknown.jpg")

