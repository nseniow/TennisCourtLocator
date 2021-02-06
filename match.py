import cv2 as cv
import numpy as np
import glob
import math
from utilities import *

def find_tennis_court_breadcrumb():

    template1 = cv.imread('images/court1.png')
    template2 = cv.imread('images/court2.png')
    template3 = cv.imread('images/court3.png')
    template4 = cv.imread('images/court4.png')
    temp1 = cv.cvtColor(template1, cv.COLOR_BGR2GRAY)
    temp2 = cv.cvtColor(template2, cv.COLOR_BGR2GRAY)
    temp3 = cv.cvtColor(template3, cv.COLOR_BGR2GRAY)
    temp4 = cv.cvtColor(template4, cv.COLOR_BGR2GRAY)

    template = [temp1, temp2, temp3, temp4]

    imagepath = ".\images\sateliteimage*.png"
    images = glob.glob(imagepath)

    final_result_list = []
    for image in images:
        img_rgb = cv.imread(image)
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

        name_parse = image[:-4].split("_")
        centerXCord = float(name_parse[1])
        centerYCord = float(name_parse[2])

        found_court = False
        for temp in template:

            w, h = temp1.shape[::-1]
            res = cv.matchTemplate(img_gray, temp, cv.TM_CCOEFF_NORMED)
            threshold = 0.9
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                found_court = True
                cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255),
                             2)

        if found_court:
            labeled_file_name = "./labeled_images/" + str(centerXCord) + "_" + str(
                centerYCord) + "_" + "labeled.png"
            cv.imwrite(labeled_file_name, img_rgb)
            final_result_list.append((centerXCord, centerYCord, pt[0], pt[1]))

    with_offsets = list(map(apply_offset_to_coordinates, final_result_list))

    for i in range(0, len(with_offsets)):
        with_offsets[i] = str(with_offsets[i])[1:-1].replace(" ", "")

    return with_offsets



print(find_tennis_court_breadcrumb())