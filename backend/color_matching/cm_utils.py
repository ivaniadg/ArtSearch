import os

import matplotlib.pyplot as plt
from colorthief import ColorThief
import pickle
import cv2
import os
from colour import Color
import math


def process_folder(path):
    # initialize the index dictionary to store the image name
    # and corresponding histograms and the images dictionary
    # to store the images themselves
    index = {}
    images = {}

    for i, image_name in enumerate(os.listdir(path)):
        if image_name.endswith(".png") or image_name.endswith(".jpg") or image_name.endswith(".jpeg"):
            # if i == 5:
            #     break
            # hist = test(path + image_name)
            color_thief = ColorThief(path + image_name)
            palette = color_thief.get_palette(color_count=6)
            print(i)
            index[path + image_name] = palette

    save_data(index)
    return index


def save_data(data):
    with open('color_matching/output/colors.pickle', 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_data():
    file_path = os.path.join(os.path.dirname(__file__), 'output', 'colors.pickle')

    with open(file_path, 'rb') as handle:
        return pickle.load(handle)


def test(im):
    image = cv2.imread(im)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist(image, [0, 1], None, [50, 10],
                        [0, 180, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist


def get_histogram(image_path):
    image = cv2.imread(image_path)
    hist = cv2.calcHist(image, [0, 1], None, [50, 50, 50],
                        [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist


def find_matches(input_image_path, data):
    input_hist = test(input_image_path)
    results = {}
    # loop over the index
    for (k, hist) in data.items():
        # compute the distance between the two histograms
        # using the method and update the results dictionary
        d = cv2.compareHist(input_hist, hist, cv2.HISTCMP_CORREL)
        # d = cv2.compareHist(input_hist, hist, cv2.HISTCMP_KL_DIV)
        results[k] = d
    # sort the results
    results = sorted([(v, k) for (k, v) in results.items()], reverse=False)

    return results


def calculate_percentage(results):
    maximum = 0
    # print(results)
    for (path, value) in results.items():
        # print(value)
        maximum = max(maximum, value)

    # total = sum(val for _, val in results.items())
    return [(key, 1 - val / maximum) for key, val in results.items()]


def find_matches2(input_image_path, data):
    color_thief = ColorThief(input_image_path)
    input_palette = color_thief.get_palette(color_count=6)
    results = {}
    # loop over the index
    for (k, palette) in data.items():
        # print(k)
        # compute the distance between the two histograms
        # using the method and update the results dictionary
        d = compare_colorpalettes(input_palette, palette)

        results[k] = d
    # sort the results
    # print(results)

    results = calculate_percentage(results)
    # print(results)
    results = sorted([(v, k) for (k, v) in results], reverse=False)
    return results


def get_color_scores(colors):
    data = load_data()
    results = {}
    # loop over the index
    for (k, palette) in data.items():
        # compute the distance between the two histograms
        # using the method and update the results dictionary
        d = compare_colorpalettes(colors, palette)
        results[k] = d


def plot_hist(hist):
    plt.hist(hist, 60)
    plt.show()


from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color


def compare_colorpalettes(palette1, palette2):
    # Initialize a variable to store the total distance
    total_distance = 0

    # Iterate over the pairs of colors in the palettes
    for rgb1, rgb2 in zip(palette1, palette2):
        # Convert the RGB values to sRGB colors
        srgb1 = sRGBColor(*rgb1)
        srgb2 = sRGBColor(*rgb2)

        # Convert the sRGB colors to CIELAB colors
        lab1 = convert_color(srgb1, LabColor)
        lab2 = convert_color(srgb2, LabColor)

        # Calculate the Euclidean distance between the colors
        distance = ((lab1.lab_l - lab2.lab_l) ** 2 + (lab1.lab_a - lab2.lab_a) ** 2 + (
                lab1.lab_b - lab2.lab_b) ** 2) ** 0.5

        # Add the distance to the total
        total_distance += distance

    return total_distance


def get_color_score(image_path):
    color_thief = ColorThief(image_path)
    palette = color_thief.get_palette(color_count=6)
    data = load_data()
    return palette, calculate_matches2(palette, data)


def analyze_colors(image):
    color_thief = ColorThief(image)
    palette = color_thief.get_palette(color_count=6)
    # add booleans to palette
    results = []
    for color in palette:
        results.append({"color": color, "bool": True})

    return results


def euclidean_distance(color1, color2):
    return math.sqrt((color1[0] - color2[0]) ** 2 + (color1[1] - color2[1]) ** 2 + (color1[2] - color2[2]) ** 2)


def color_palette_similarity(palette1, palette2):
    similarity = 0
    for color1 in palette1:
        min_distance = float('inf')
        for color2 in palette2:
            distance = euclidean_distance(color1, color2)
            if distance < min_distance:
                min_distance = distance
        similarity += min_distance
    #In the RGB color space, the maximum distance between two colors is approximately 441.67 (sqrt(255^2 + 255^2 + 255^2)).
    max_similarity = 441.67 * len(palette1)
    return  1 - (similarity / max_similarity)


def calculate_matches2(colors, data) -> dict:
    distances = {}
    for (k,palette) in data.items():
        distance = 0
        for i in range(len(colors)):
            distance += euclidean_distance(colors[i], palette[i])
        distances[k] = distance
    # sort the results dictionary reverse
    sorted_indices = sorted([(v, k) for (k, v) in distances.items()])
    #normalize the distances
    max_distance = sorted_indices[-1][0]
    sorted_indices = [(v / max_distance, k) for (v, k) in sorted_indices]

    # set matching percentage
    sorted_indices = [(1 - v, k) for (v, k) in sorted_indices]
    # return the sorted results as dictionary
    return {k: v for (v, k) in sorted_indices}

def calculate_matches(colors, data) -> dict:
    results = {}
    # loop over the index
    for (k, palette) in data.items():
        # compute the distance between the two histograms
        # using the method and update the results dictionary
        d = color_palette_similarity(colors, palette)
        results[k] = d
    return results


def get_color_scores(colors):
    x = load_data()
    return calculate_matches(colors, x)

def get_precalc_scores(image_name):
    x = load_data()
    colors = x[image_name]
    return colors,calculate_matches(colors, x)
