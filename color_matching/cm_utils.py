import os
from colorthief import ColorThief
import pickle

def process_folder(path):
    list = []
    for i, image in enumerate(os.listdir(path)):
        print(i)
        if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg"):
            color_thief = ColorThief('/home/mortirreke/Desktop/assets/images_2673.jpg')
            dominant_colors = color_thief.get_palette(color_count=6)
            list.append((dominant_colors, path + image))
    save_data(list)
    return list


def save_data(data):
    with open('object_detection/output/colors.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_data():
    with open('object_detection/output/colors.pickle', 'rb') as handle:
        return pickle.load(handle)



def get_score(list1,list2):
    score = 0
    inputcopy = copy.copy(list1)
    for object2 in list2:
        for object1 in inputcopy:
            if object1 == object2:
                inputcopy.remove(object1)
                score = score + 1
    return score