import math

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread('images/map1.png', 0)
# img = cv.medianBlur(img,5)
# ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
# th2 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_MEAN_C,\
#             cv.THRESH_BINARY,11,2)
# th3 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
#             cv.THRESH_BINARY_INV,11,15)
# titles = ['Original Image', 'Global Thresholding (v = 127)',
#             'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images = [img, th1, th2, th3]
# for i in range(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()

# cv.imshow('threshold.png', th3)

# img = th3
cannyThres1 = 200
cannyThres2 = 200
edges = cv.Canny(img, cannyThres1, cannyThres2)
plt.subplot(122), plt.imshow(edges, cmap='gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
# plt.show()


cv.imwrite("edges.png", edges)

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 30  # minimum number of pixels making up a line
max_line_gap = 12  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on
lines = cv.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                       min_line_length, max_line_gap)

short_lines = []
long_lines = []
for line in lines:
    for x1, y1, x2, y2 in line:
        distance = np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))
        angle = math.atan2(y2 - y1, x2 - x1)
        if angle > math.pi:
            angle = angle - math.pi
        if 40 < distance < 50:
            short_lines.append((x1, y1, x2, y2, angle))
            # cv.line(line_image,(x1,y1),(x2,y2),(255,0,0), 1)
        elif 100 < distance < 120:
            long_lines.append((x1, y1, x2, y2, angle))
            # cv.line(line_image,(x1,y1),(x2,y2),(255,0,0), 1)


def distance(x1, y1, x2, y2):
    return np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))


long_lines.sort(key=lambda x: x[4])

count = 0
adjacency = 10
parallel_long_pairs = []
for i in range(len(long_lines)):
    fx1, fy1, fx2, fy2, fangle = long_lines[i]
    for j in range(i + 1, min(len(long_lines), i + adjacency)):
        sx1, sy1, sx2, sy2, sangle = long_lines[j]
        # Check parallel
        if (abs(fangle - sangle) < math.pi / 30):
            count = count + 1
            # Check distance four possibilities
            firstDist = distance(fx1, fy1, sx1, sy1)
            secondDist = distance(fx1, fy1, sx2, sy2)
            thirdDist = distance(fx2, fy2, sx1, sy1)
            fourthDist = distance(fx2, fy2, sx2, sy2)
            if 40 < firstDist < 60 and 40 < fourthDist < 60:
                # cv.line(line_image,(sx1,sy1),(sx2,sy2),(255,0,0), 1)
                # cv.line(line_image, (fx1, fy1), (fx2, fy2), (255, 0, 0), 1)
                parallel_long_pairs.append(
                    ((fx1, fy1), (sx1, sy1), (fx2, fy2), (sx2, sy2)))
            elif 40 < secondDist < 60 and 40 < thirdDist < 60:
                # cv.line(line_image, (sx1, sy1), (sx2, sy2), (255, 0, 0), 1)
                # cv.line(line_image, (fx1, fy1), (fx2, fy2), (255, 0, 0), 1)
                parallel_long_pairs.append(
                    ((fx1, fy1), (sx2, sy2), (fx2, fy2), (sx1, sy1)))

for i in range(len(parallel_long_pairs)):
    (fx1, fy1), (sx1, sy1), (fx2, fy2), (sx2, sy2) = parallel_long_pairs[i]

    # the first two connects, the last two connects
    firstConnector = None
    for shortx1, shorty1, shortx2, shorty2, _ in short_lines:
        # Check first pair
        dist1 = distance(fx1, fy1, shortx1, shorty1)
        dist2 = distance(fx1, fy1, shortx2, shorty2)
        dist3 = distance(sx1, sy1, shortx1, shorty1)
        dist4 = distance(sx1, sy1, shortx2, shorty2)

        if dist1 < 10 and dist4 < 10:
            firstConnector = (shortx1, shorty1, shortx2, shorty2)
        elif dist2 < 10 and dist3 < 10:
            firstConnector = (shortx1, shorty1, shortx2, shorty2)

    if firstConnector == None:
        continue

    secondConnector = None
    for shortx1, shorty1, shortx2, shorty2, _ in short_lines:
        dist1 = distance(fx2, fy2, shortx1, shorty1)
        dist2 = distance(fx2, fy2, shortx2, shorty2)
        dist3 = distance(sx2, sy2, shortx1, shorty1)
        dist4 = distance(sx2, sy2, shortx2, shorty2)

        if dist1 < 10 and dist4 < 10:
            secondConnector = (shortx1, shorty1, shortx2, shorty2)
        elif dist2 < 10 and dist3 < 10:
            secondConnector = (shortx1, shorty1, shortx2, shorty2)

    if secondConnector == None:
        continue

    cv.line(line_image, (firstConnector[0], firstConnector[1]),
            (firstConnector[2], firstConnector[3]), (255, 0, 0), 3)
    cv.line(line_image, (secondConnector[0], secondConnector[1]),
            (secondConnector[2], secondConnector[3]), (255, 0, 0), 3)
    cv.line(line_image, (fx1, fy1), (fx2, fy2), (255, 0, 0), 3)
    cv.line(line_image, (sx1, sy1), (sx2, sy2), (255, 0, 0), 3)

lines_edges = cv.addWeighted(img, 0.8, line_image, 1, 0)

cv.imwrite("lines.png", lines_edges)
