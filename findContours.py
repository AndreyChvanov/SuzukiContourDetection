import numpy as np


class Neighborhoods:
    def __init__(self):
        self.clockwise_path = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]
        self.counterclockwise_path = self.clockwise_path[::-1]

    def get_neighborhoods(self, p2, p3, order_type):
        if order_type == "cw":
            path = self.clockwise_path
        else:
            path = self.counterclockwise_path
        start_position = path.index([p2[0] - p3[0], p2[1] - p3[1]])
        for step in range(start_position + 1, len(path) + start_position + 1):
            i, j = p3[0] + path[step % len(path)][0], p3[1] \
                   + path[step % len(path)][1]
            yield i, j


class Border:
    def __init__(self, border_type, parent, NBD):
        self.type = border_type
        self.parent = parent
        self.NBD = abs(NBD)


class ContoursFinder:
    def __init__(self):
        self.neighborhoods = Neighborhoods()

    def __get_work_pixel(self, binary_image, start_pixel, cur_pixel):
        for i, j in self.neighborhoods.get_neighborhoods(start_pixel, cur_pixel, order_type="cw"):
            if binary_image[i, j] != 0:
                return (i, j)
        return None

    def __get_next_pixel(self, binary_image, p2, p3):
        p4, right_neighborhood = None, None
        for i, j in self.neighborhoods.get_neighborhoods(p2, p3, order_type="ccw"):
            if i < 0 or i >= binary_image.shape[0] or j < 0 or j >= binary_image.shape[1]:
                continue
            if binary_image[i, j] != 0:
                if p3[1] + 1 <= binary_image.shape[1] - 1:
                    right_neighborhood = (p3[0], p3[1] + 1)
                p4 = (i, j)
                break
        return p4, right_neighborhood

    def __define_border_parrent(self, border):
        border_ = None
        for prev_border in self.borders:
            if prev_border.NBD == self.LNBD:
                border_ = prev_border
                break
        if (border.type == "a" and border_.type == "a") \
                or (border.type == "b" and border_.type == "b"):
            border.parent = border_.parent
        else:
            border.parent = self.LNBD

    def __scan_border(self, binary_image, start_pixel, cur_pixel, NBD, border_type):
        border = Border(border_type, None, NBD)
        self.borders.append(border)
        self.__define_border_parrent(border)
        work_pixel = self.__get_work_pixel(binary_image, start_pixel, cur_pixel)
        if work_pixel is None:
            binary_image[cur_pixel[0], cur_pixel[1]] = -NBD
        else:
            p2, p3 = work_pixel, cur_pixel
            while True:
                p4, right_neighborhood = self.__get_next_pixel(binary_image, p2, p3)
                if p4 is None:
                    break
                if right_neighborhood is not None:
                    if binary_image[right_neighborhood[0], right_neighborhood[1]] == 0:
                        binary_image[p3[0], p3[1]] = -NBD
                    elif binary_image[p3[0], p3[1]] == 1:
                        binary_image[p3[0], p3[1]] = NBD
                if p4 == cur_pixel and p3 == work_pixel:
                    break
                p2 = p3
                p3 = p4

    def __call__(self, binary_image):
        NBD = 1
        self.LNBD = 1
        self.borders = [Border('frame', None, 1)]
        for i in range(0, binary_image.shape[0]):
            self.LNBD = 1
            for j in range(0, binary_image.shape[1] - 1):
                if binary_image[i, j] == 0:
                    continue
                if binary_image[i, j] == 1 and binary_image[i, j - 1] == 0:
                    NBD += 1
                    self.__scan_border(binary_image, (i, j - 1), (i, j), NBD, border_type="a")
                elif binary_image[i, j] >= 1 and binary_image[i, j + 1] == 0:
                    NBD += 1
                    if binary_image[i, j] > 1:
                        self.LNBD = binary_image[i, j]
                    self.__scan_border(binary_image, (i, j + 1), (i, j), NBD, border_type="b")
                elif binary_image[i, j] != 1:
                    self.LNBD = abs(binary_image[i, j])
        f = binary_image
        binary_image = np.abs(binary_image)
        contours = [(binary_image == i).astype(np.uint8) for i in range(2, f.max() + 1)]
        return f, contours, self.borders
