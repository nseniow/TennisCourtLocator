import math

import numpy as np

def distance(x1, y1, x2, y2):
    return np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))

def add_meters_to_coordinates(coordinates, long_offset, lat_offset): #should be 275 meters?
    lat = coordinates[0]
    long = coordinates[1]
    R = 6378137

    dLat = lat_offset / R
    dLong = long_offset / (R * math.cos(math.pi * lat / 180))

    latO = lat + dLat * 180/math.pi
    longO = long + dLong * 180/math.pi

    return round(latO, 6), round(longO, 6)


def apply_offset_to_coordinates(tup):
    lat, long, xoffset, yoffset = tup

    yoffset -= 1280/2
    xoffset -= 1280/2

    yoffset *= -275/1280
    xoffset *= 275/1280

    print("X", xoffset)
    print("Y", yoffset)


    return add_meters_to_coordinates((lat, long), xoffset, yoffset)
