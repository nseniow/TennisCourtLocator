import urllib.request
import numpy
import math
import time
import random

f = open("apikey.txt", "r")
apikey = f.read()

def add_meters_to_coordinates(coordinates, long_offset, lat_offset): #should be 275 meters?
    lat = coordinates[0]
    long = coordinates[1]
    R = 6378137

    dLat = lat_offset / R
    dLong = long_offset / (R * math.cos(math.pi * lat / 180))

    latO = lat + dLat * 180/math.pi
    longO = long + dLong * 180/math.pi

    return round(latO, 6), round(longO, 6)



def download_image(lat, long, zoom = 18, size = 640, scale = 2, maptype = "satellite", key = apikey):
    image_url = "https://maps.googleapis.com/maps/api/staticmap?center=" + str(lat) + "," + str(long) + "&zoom=" + str(zoom) + "&scale=" + str(scale) + "&size=" + str(size) + "x" + str(size) + "&maptype=" + maptype + "&key=" + key


    urllib.request.urlretrieve(image_url, "./images/sateliteimage_" + str(lat) + "_" + str(long) + ".png")


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

    while current_long < add_meters_to_coordinates((max_lat, max_long), -275/2, 0)[1]:
        while current_lat < add_meters_to_coordinates((max_lat, max_long), 0, -275/2)[0]:
            all_coordinates.append((current_lat, current_long))
            current_lat = add_meters_to_coordinates((current_lat, current_long), 0, 275)[0]
        current_long = add_meters_to_coordinates((current_lat, current_long), 275, 0)[1]
        current_lat = min_lat

    return all_coordinates


def save_images_from_coordinates(coordinates):
    bouding_rectangle = get_bounding_rectangle(coordinates)
    all_image_coordinates = get_all_image_coordinates_from_bounding_rectangle(bouding_rectangle)
    for i in all_image_coordinates:
        random_delay = random.randint(5000,15000)
        time.sleep(random_delay/1000)
        download_image(i[0], i[1])
        print("downloaded: " + str(i[0]) + "_" + str(i[1]) + " after a delay of " + str(random_delay))
    return true



coordinates = [
      [
        -79.4712353,
        43.9066741
      ],
      [
        -79.4245434,
        43.9095186
      ],
      [
        -79.4215393,
        43.8933155
      ],
      [
        -79.4673729,
        43.8907176
      ]
    ]

'''
LINESTRING(23.39843571186064 31.797305887523642,43.261716961860635 29.299828995609584,43.701170086860635 18.306570219206368,27.79296696186064 11.77489027239198,23.22265446186064 21.61046809283413,23.39843571186064 31.797305887523642)
POLYGON((19.70702946186064 24.521154410428796,29.19921696186064 33.57253803233765,38.076170086860635 27.833263305312435,35.615232586860635 18.556715890729684,46.777341961860635 25.318224647264405,50.644529461860635 11.430512243985506,24.45312321186064 7.79156584494485,24.36523258686064 19.96717062175542,19.70702946186064 24.521154410428796))
POLYGON((-79.62021729531205 44.16191319112033,-79.2878808695308 44.16191319112033,-79.2878808695308 43.97838830602814,-79.62021729531205 43.97838830602814,-79.62021729531205 44.16191319112033))
'''

def convert_input_string_to_coordinate_list(input_string):
    if input_string.startswith("LINESTRING"):
        input_string = input_string[11:-1]
        print(input_string)
    elif input_string.startswith("POLYGON"):
        print("Poly")
    else:
        print("Error")

convert_input_string_to_coordinate_list("LINESTRING(23.39843571186064 31.797305887523642,43.261716961860635 29.299828995609584,43.701170086860635 18.306570219206368,27.79296696186064 11.77489027239198,23.22265446186064 21.61046809283413,23.39843571186064 31.797305887523642)")

#save_images_from_coordinates(coordinates)



