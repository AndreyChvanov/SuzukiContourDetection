import numpy as np
import cv2

th_low = np.array([39, 40, 0])
th_up = np.array([80, 220, 160])

bbox_low_th = [220, 240] # h, w
bbox_up_th = [500, 800]


def load_image(path):
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_blur = cv2.GaussianBlur(img_rgb, (23,23), 160)
    return cv2.cvtColor(img_blur, cv2.COLOR_RGB2HSV), img_rgb


def get_color_mask_by_image(img_hsv):
    mask = cv2.inRange(img_hsv, th_low, th_up)
    mask = (mask/255).astype(np.int16)
    return mask


def get_bb_of_contours(contours):
    bounding_boxes = []
    for c in contours:
        x, y, h, w = cv2.boundingRect(c)
        if bbox_low_th[0] <= h <= bbox_up_th[0] and bbox_low_th[1] <= w <= bbox_up_th[1]:
            bounding_boxes.append([x, y, x+h, y+w])
    return bounding_boxes


def draw_bounding_boxes(image, bounding_boxes):
    for bb in bounding_boxes:
        x1, y1, x2, y2 = bb[0], bb[1], bb[2], bb[3]
        cv2.rectangle(image, (x2, y2), (x1, y1), (255, 0, 0,), 2)


def save_image(image, name):
    cv2.imwrite(name, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))



