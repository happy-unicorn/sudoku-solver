import math
import numpy as np
import cv2


class PreImageService:
    def __init__(self, file):
        self.__image = self.__load(file)
        self.__original_image = self.__image.copy()

    def pre_numbers(self):
        self.__filters()
        self.__get_contours()
        self.__transformed_filters()
        self.__resize()
        img = self.__image.copy()

        number_of_elem = 9
        height, width = img.shape
        delta_height, delta_width = math.floor(height / number_of_elem), math.floor(width / number_of_elem)
        numbers_grid = []
        for i in range(number_of_elem):
            row_grid = []
            for j in range(number_of_elem):
                number = img[
                         i * delta_height: (i + 1) * delta_height,
                         j * delta_width: (j + 1) * delta_width]
                row_grid.append(number)
            numbers_grid.append(row_grid)

        test_grid = []
        for row in numbers_grid:
            row_grid = []
            for elem in row:
                for i in range(12, 18):
                    for j in range(12, 18):
                        if elem[i][j] == 255:
                            cv2.floodFill(elem, None, (j, i), 127)
                for i in range(28):
                    for j in range(28):
                        elem[i][j] = 255 if elem[i][j] == 127 else 0
                if (elem.mean() < 10):
                    elem = np.zeros((28, 28))
                else:
                    cnts = cv2.findContours(elem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
                    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
                    M = cv2.moments(cnts[0])
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    elem = np.roll(elem, 13 - cY, 0)
                    elem = np.roll(elem, 13 - cX, 1)
                row_grid.append(elem)
            test_grid.append(row_grid)

        return test_grid

    def __load(self, file):
        return cv2.imdecode(np.fromstring(file, np.uint8), cv2.IMREAD_UNCHANGED)

    def __resize(self):
        self.__image = cv2.resize(self.__image, (252, 252))
        self.__image = cv2.threshold(self.__image, 127, 255, cv2.THRESH_BINARY)[1]

    def __filters(self):
        self.__image = cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)
        self.__image = cv2.medianBlur(self.__image, 3)
        self.__image = cv2.adaptiveThreshold(self.__image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 3)

    def __transformed_filters(self):
        self.__image = cv2.cvtColor(self.__image, cv2.COLOR_BGR2GRAY)
        self.__image = cv2.GaussianBlur(self.__image, (11, 11), 0)
        self.__image = cv2.adaptiveThreshold(self.__image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    def __get_contours(self):
        cnts = cv2.findContours(self.__image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.015 * peri, True)
            self.__image = self.__perspective_transform(approx)
            break

    def __perspective_transform(self, corners):
        def order_corner_points(corners):
            corners = [(corner[0][0], corner[0][1]) for corner in corners]
            top_r, top_l, bottom_l, bottom_r = corners[0], corners[1], corners[2], corners[3]
            return (top_l, top_r, bottom_r, bottom_l)

        ordered_corners = order_corner_points(corners)
        top_l, top_r, bottom_r, bottom_l = ordered_corners

        width_A = np.sqrt(((bottom_r[0] - bottom_l[0]) ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
        width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
        width = max(int(width_A), int(width_B))

        height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) + ((top_r[1] - bottom_r[1]) ** 2))
        height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) + ((top_l[1] - bottom_l[1]) ** 2))
        height = max(int(height_A), int(height_B))

        dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
        ordered_corners = np.array(ordered_corners, dtype="float32")
        matrix = cv2.getPerspectiveTransform(ordered_corners, dimensions)
        return cv2.warpPerspective(self.__original_image, matrix, (width, height))
