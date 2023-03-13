import os
import pickle

#function that saves all image names of a folder in a list and saves it to a pickle file
def get_image_names():
    names = []
    for i, image in enumerate(os.listdir("/home/mortirreke/Desktop/assets/")):
        if image.endswith(".png") or image.endswith(".jpg") or image.endswith(".jpeg"):
            names.append(image)
    with open('imagelist.pickle', 'wb') as handle:
        pickle.dump(names, handle, protocol=pickle.HIGHEST_PROTOCOL)

get_image_names()