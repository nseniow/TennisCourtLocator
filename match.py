import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import glob


img_rgb = cv.imread('images/testcourts1.png')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)


template1 = cv.imread('images/courts/court1.png')
template2 = cv.imread('images/courts/court2.png')
template3 = cv.imread('images/courts/court3.png')
template4 = cv.imread('images/courts/court4.png')
temp1 = cv.cvtColor(template1, cv.COLOR_BGR2GRAY)
temp2 = cv.cvtColor(template2, cv.COLOR_BGR2GRAY)
temp3 = cv.cvtColor(template3, cv.COLOR_BGR2GRAY)
temp4 = cv.cvtColor(template4, cv.COLOR_BGR2GRAY)

template = [temp1, temp2, temp3, temp4]

imagepath = ".\images\courts\map*.png"
images = glob.glob(imagepath)

for image in images:
    img_rgb = cv.imread(image)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    print(image)

    for temp in template:

        w, h = temp1.shape[::-1]
        res = cv.matchTemplate(img_gray,temp,cv.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

            print("X: ", pt[0], "Y: ", pt[1])
