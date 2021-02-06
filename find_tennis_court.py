import glob
import math
import cv2 as cv
import numpy as np

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


def distance(x1, y1, x2, y2):
    return np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))


def scan_courts_in_image(image_filename):

    name_parse = image_filename[:-4].split("_")
    centerXCord = float(name_parse[1])
    centerYCord = float(name_parse[2])

    img_color = cv.imread(image_filename)
    img = cv.imread(image_filename, 0)
    cannyThres1 = 200
    cannyThres2 = 200
    edges = cv.Canny(img, cannyThres1, cannyThres2)
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 25  # minimum number of pixels making up a line
    max_line_gap = 12  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img_color) * 0  # creating a blank to draw lines on
    lines = cv.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                           min_line_length, max_line_gap)
    short_lines = []
    long_lines = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            length = distance(x1, y1, x2, y2)
            angle = math.atan2(y2 - y1, x2 - x1)
            if angle > math.pi:
                angle = angle - math.pi
            if 40 < length < 55:
                short_lines.append((x1, y1, x2, y2, angle))
                # cv.line(line_image,(x1,y1),(x2,y2),(255,0,0), 1)
            elif 100 < length < 120:
                long_lines.append((x1, y1, x2, y2, angle))
                # cv.line(line_image,(x1,y1),(x2,y2),(255,0,0), 1)

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
                if 40 < firstDist < 65 and 40 < fourthDist < 65:
                    # cv.line(line_image,(sx1,sy1),(sx2,sy2),(255,0,0), 1)
                    # cv.line(line_image, (fx1, fy1), (fx2, fy2), (255, 0, 0), 1)

                    parallel_long_pairs.append(
                        ((fx1, fy1), (sx1, sy1), (fx2, fy2), (sx2, sy2), fangle))
                elif 40 < secondDist < 65 and 40 < thirdDist < 65:
                    # cv.line(line_image, (sx1, sy1), (sx2, sy2), (255, 0, 0), 1)
                    # cv.line(line_image, (fx1, fy1), (fx2, fy2), (255, 0, 0), 1)
                    parallel_long_pairs.append(
                        ((fx1, fy1), (sx2, sy2), (fx2, fy2), (sx1, sy1), fangle))

    court_found = False
    for i in range(len(parallel_long_pairs)):
        (fx1, fy1), (sx1, sy1), (fx2, fy2), (sx2, sy2), long_angle = \
            parallel_long_pairs[i]

        # the first two connects, the last two connects
        firstConnector = None
        for shortx1, shorty1, shortx2, shorty2, angle in short_lines:
            # Check first pair

            if not -0.1 < math.cos(angle - long_angle) < 0.1:
                continue

            dist1 = distance(fx1, fy1, shortx1, shorty1)
            dist2 = distance(fx1, fy1, shortx2, shorty2)
            dist3 = distance(sx1, sy1, shortx1, shorty1)
            dist4 = distance(sx1, sy1, shortx2, shorty2)

            if dist1 < 15 and dist4 < 15:
                firstConnector = (shortx1, shorty1, shortx2, shorty2)
            elif dist2 < 15 and dist3 < 15:
                firstConnector = (shortx1, shorty1, shortx2, shorty2)

        if firstConnector == None:
            continue

        secondConnector = None
        for shortx1, shorty1, shortx2, shorty2, angle in short_lines:

            if not -0.1 < math.cos(angle - long_angle) < 0.1:
                continue

            dist1 = distance(fx2, fy2, shortx1, shorty1)
            dist2 = distance(fx2, fy2, shortx2, shorty2)
            dist3 = distance(sx2, sy2, shortx1, shorty1)
            dist4 = distance(sx2, sy2, shortx2, shorty2)

            if dist1 < 15 and dist4 < 15:
                secondConnector = (shortx1, shorty1, shortx2, shorty2)
            elif dist2 < 15 and dist3 < 15:
                secondConnector = (shortx1, shorty1, shortx2, shorty2)

        if secondConnector == None:
            continue

        cv.line(line_image, (firstConnector[0], firstConnector[1]),
                (firstConnector[2], firstConnector[3]), (255, 0, 0), 3)
        cv.line(line_image, (secondConnector[0], secondConnector[1]),
                (secondConnector[2], secondConnector[3]), (255, 0, 0), 3)
        cv.line(line_image, (fx1, fy1), (fx2, fy2), (255, 0, 0), 3)
        cv.line(line_image, (sx1, sy1), (sx2, sy2), (255, 0, 0), 3)

        court_found = True

    if court_found:
        img = cv.imread(image_filename)
        lines_edges = cv.addWeighted(img, 0.8, line_image, 1, 0)
        labeled_file_name = "./labeled_images/" + str(centerXCord) + "_" + str(centerYCord) + "_" + "labeled.png"
        cv.imwrite(labeled_file_name, lines_edges)

        return centerXCord, centerYCord, fx1, fy1

    return None

## Return a list of tuple coordinates
# [(centerXCord, centerYCord, pixelsX, pixelsY), (centerXCord, centerYCord, pixelsX, pixelsY) ...]
def find_tennis_court(list_of_images=None):
    imagepath = ".\images\sateliteimage*.png"
    images = glob.glob(imagepath)

    final_result_list = []
    for image in images:

        result = scan_courts_in_image(image)

        if result is not None:
            final_result_list.append(result)

    return final_result_list

a = find_tennis_court()
print(a)
print(list(map(apply_offset_to_coordinates, a)))
