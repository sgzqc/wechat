import os
import cv2
import sys
import numpy as np


def show_img(net_width,net_height,rect1,rect2):
    show_img = np.zeros((net_height,net_width,3),np.uint8)
    for i in range(4):
        cv2.line(show_img,(rect1[i*2], rect1[i*2+1]), (rect1[(i*2+2)%8], rect1[(i*2+3)%8]), color=(0, 0 ,255), thickness=2)
    for i in range(4):
        cv2.line(show_img,(rect2[i*2], rect2[i*2+1]), (rect2[(i*2+2)%8], rect2[(i*2+3)%8]), color=(0, 255 ,0), thickness=2)
    return show_img


def draw_region(img,rect_1,rect_2=None,fill_value=255):
    pt_list = list()
    for i in range(4):
        pt_list.append((rect_1[i*2],rect_1[i*2+1]))
    cv2.fillPoly(img, [np.array(pt_list)], fill_value)
    if rect_2 is not None:
        pt_list2 = list()
        for i in range(4):
            pt_list2.append((rect_2[i * 2], rect_2[i * 2 + 1]))
        cv2.fillPoly(img, [np.array(pt_list2)], fill_value)
    return img


def compute_iou(net_width,net_height,rect1,rect2,fill_value=255):
    img1 = np.zeros((net_height, net_width), np.uint8)
    img2 = np.zeros((net_height, net_width), np.uint8)
    img3 = np.zeros((net_height, net_width), np.uint8)
    out_img1 = draw_region(img1, rect1, fill_value=fill_value)
    out_img2 = draw_region(img2, rect2, fill_value=fill_value)
    out_img3 = draw_region(img3, rect1, rect2, fill_value=fill_value)
    area_1 = np.sum(out_img1 == fill_value)
    area_2 = np.sum(out_img2 == fill_value)
    area_com = np.sum(out_img3 == fill_value)
    print("area1 ={} area2={} area3={} ".format(area_1, area_2, area_com))
    iou = (area_1 + area_2 - area_com) * 1.0 / area_com
    return iou


if __name__ == "__main__":
    net_width = 320
    net_height = 320
    rect1 = [160,100, 120,220, 200,220, 180, 100]
    rect2 = [180,150, 150,250, 220,250, 230 ,152]
    out_img = show_img(net_width, net_height, rect1, rect2)
    iou = compute_iou(net_width,net_height,rect1,rect2)
    print("iou={}".format(iou))
    cv2.imshow("org", out_img)
    cv2.waitKey(0)

