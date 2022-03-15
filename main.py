from DIP_Task1.findContours import ContoursFinder
from DIP_Task1 import utils
import numpy as np
import cv2

if __name__ == '__main__':
    img_hsv, img_rgb = utils.load_image("images/segment.jpg")
    color_mask = utils.get_color_mask_by_image(img_hsv)
    cv2.imwrite("mask.png", np.uint8(color_mask)*255)
    finder = ContoursFinder()
    f, contours, borders = finder(color_mask)
    f = np.abs(f)
    f[f == 1] = 0
    f[f > 1] = 255
    cv2.imwrite("contours.png", np.uint8(f))
    filer_bounding_boxes = utils.get_bb_of_contours(contours)
    utils.draw_bounding_boxes(img_rgb, filer_bounding_boxes)
    utils.save_image(img_rgb, "result_bb.png")






