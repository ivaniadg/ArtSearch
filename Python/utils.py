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


#function that gets artist and title from image name (format: artist_title.jpg) or unknown if no artist or title is found
def get_metadata(image_name):
    #check if image name contains an underscore and doesnt start with "images"
    if "_" in image_name and not image_name.startswith("images"):
        #split image name at underscore and get artist and title
        artist = image_name.split("_")[0]
        title = image_name.split("_")[1].split(".")[0]
        #replace - with space
        artist = artist.replace("-", " ")
        title = title.replace("-", " ")
        return {"artist": artist, "title": title}
    else:
        return {"artist": "unknown", "title": "unknown"}