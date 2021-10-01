import os
import cv2
import math
import numpy as np


def get_demo(img,label,out_width,out_height):
    out_radius = out_width if out_width< out_height else out_height
    small_img   = cv2.resize(img,   (out_radius, out_radius))
    small_label = cv2.resize(label, (out_radius, out_radius))
    for i in range(out_height):
        for j in range(out_width):
            distance = int ( math.sqrt(i*i+j*j) )
            alpha =  1 if distance > out_radius else distance  / out_radius
            for k in range(3):
                small_label[i][j][k] = int(alpha * small_img[i][j][k] + (1-alpha) * small_label[i][j][k])
    return small_label


def get_demo2(img,label,out_width,out_height):
    out_radius =  math.sqrt(out_width * out_width + out_height * out_height)
    small_img   = cv2.resize(img,   (out_width, out_height))
    small_label = cv2.resize(label, (out_width, out_height))
    for i in range(out_height):
        for j in range(out_width):
            distance = int ( math.sqrt(i*i+j*j) )
            alpha =  1 if distance > out_radius else distance  / out_radius
            for k in range(3):
                small_label[i][j][k] = int(alpha * small_img[i][j][k] + (1-alpha) * small_label[i][j][k])
    return small_label


if __name__ == "__main__":
    img_file = "./sample/gaoyuanyuan.jpg"
    label_file = "./sample/hongqi.jpg"
    img = cv2.imread(img_file)
    label = cv2.imread(label_file)
    out_width = 300
    out_height =300

    out_img1 = get_demo(img, label, out_width, out_height)
    out_img2 = get_demo2(img,label,out_width,out_height)



    cv2.imshow("out1", out_img1)
    cv2.imshow("out2", out_img2)
    cv2.waitKey(0)
