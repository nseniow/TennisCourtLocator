import urllib.request
import numpy
import math
import time
import random
import re
import itertools
from utilities import *

f = open("apikey.txt", "r")
apikey = f.read()


def download_image(lat, long, zoom = 18, size = 640, scale = 2, maptype = "satellite", key = apikey):
    image_url = "https://maps.googleapis.com/maps/api/staticmap?center=" + str(lat) + "," + str(long) + "&zoom=" + str(zoom) + "&scale=" + str(scale) + "&size=" + str(size) + "x" + str(size) + "&maptype=" + maptype + "&key=" + key

    urllib.request.urlretrieve(image_url, "./images/sateliteimage_" + str(lat) + "_" + str(long) + ".png")
    return "./images/sateliteimage_" + str(lat) + "_" + str(long) + ".png"


def get_bounding_rectangle(coordinates):
    min_long = numpy.min(list(map(lambda x : x[0], coordinates)))
    max_long = numpy.max(list(map(lambda x : x[0], coordinates)))
    min_lat = numpy.min(list(map(lambda x: x[1], coordinates)))
    max_lat = numpy.max(list(map(lambda x: x[1], coordinates)))
    return((min_lat, min_long), (max_lat, max_long))

def get_all_image_coordinates_from_bounding_rectangle(bounding_rectangle):
    min_lat = add_meters_to_coordinates(bounding_rectangle[0], 0, 275/2)[0]
    min_long = add_meters_to_coordinates(bounding_rectangle[0], 275/2, 0)[1]
    max_lat = bounding_rectangle[1][0]
    max_long = bounding_rectangle[1][1]

    current_lat = min_lat
    current_long = min_long

    all_coordinates = []
    flag = True

    while flag or current_long < add_meters_to_coordinates((max_lat, max_long), -275/2, 0)[1]:
        while flag or current_lat < add_meters_to_coordinates((max_lat, max_long), 0, -275/2)[0]:
            all_coordinates.append((current_lat, current_long))
            current_lat = add_meters_to_coordinates((current_lat, current_long), 0, 275)[0]
            flag = False
        current_long = add_meters_to_coordinates((current_lat, current_long), 275, 0)[1]
        current_lat = min_lat

    return all_coordinates


def save_images_from_coordinates(coordinates):
    bouding_rectangle = get_bounding_rectangle(coordinates)
    all_image_coordinates = get_all_image_coordinates_from_bounding_rectangle(bouding_rectangle)
    filenames = []
    for i in all_image_coordinates:
        random_delay = random.randint(0,1500)
        time.sleep(random_delay/1000)
        filenames.append(download_image(i[0], i[1]))
        print("downloaded: " + str(i[0]) + "_" + str(i[1]) + " after a delay of " + str(random_delay))
    return filenames

def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))

def reverse_coordinate(coordinate):
    return [float(coordinate[0]), float(coordinate[1])]

def reverse_coordinates(coordinates):
    return list(map(reverse_coordinate, coordinates))


def convert_input_string_to_coordinate_list(input_string):
    if input_string.startswith("LINESTRING"):
        input_string = input_string[11:-1]
    elif input_string.startswith("POLYGON"):
        input_string = input_string[9:-2]
    else:
        print("Error")
        return
    input_string = input_string.replace(" ", ",")
    coordinates = input_string.split(",")
    coordinates = list(split_seq(coordinates, 2))
    coordinates = reverse_coordinates(coordinates)
    return coordinates

def WKT_to_Images(input_string):
    return save_images_from_coordinates(convert_input_string_to_coordinate_list(input_string))

#print(WKT_to_Images("POLYGON((-75.73874733380869 45.254549821048876,-75.73596856526926 45.254549821048876,-75.73596856526926 45.25331117236983,-75.73874733380869 45.25331117236983,-75.73874733380869 45.254549821048876))"))
