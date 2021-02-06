import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
img_rgb = cv.imread('images/court.png')
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)

template = cv.imread('images/new_165.png', cv.IMREAD_UNCHANGED)
channels = cv.split(template)
zero_channel = np.zeros_like(channels[0])
mask = np.array(channels[3])
template_grey = cv.imread('images/new_165.png', 0)


mask[channels[3] == 0] = 1
mask[channels[3] == 100] = 0
transparent_mask = mask

cv.imwrite("mask.png", transparent_mask)
cv.imwrite("tem_grey.png", template_grey)
cv.imwrite("img_grey.png", img_gray)

w, h = template_grey.shape[::-1]
res = cv.matchTemplate(img_gray,template_grey,cv.TM_CCORR_NORMED, mask=transparent_mask)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    print("hit")
cv.imwrite('images/res.png',img_rgb)
