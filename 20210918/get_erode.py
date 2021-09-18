import os
import sys
import numpy as np
import cv2

def get_binary_img(img):
    # gray img to bin image
    bin_img = np.zeros(shape=(img.shape), dtype=np.uint8)
    h = img.shape[0]
    w = img.shape[1]
    for i in range(h):
        for j in range(w):
            bin_img[i][j] = 0 if img[i][j] < 255 else 255
    return bin_img


def horizon_erode(bin_img):
    out_img = np.zeros(shape=bin_img.shape, dtype=np.uint8) + 255
    h = bin_img.shape[0]
    w = bin_img.shape[1]
    for i in range(h):
        for j in range(1,w-1):
            out_img[i][j]=0
            for k in range(3):
                if bin_img[i][j+k-1] > 127:
                    out_img[i][j]=255
    return out_img


def vertical_erode(bin_img):
    out_img = np.zeros(shape=bin_img.shape, dtype=np.uint8) + 255
    h = bin_img.shape[0]
    w = bin_img.shape[1]
    for i in range(1,h-1):
        for j in range(w):
            out_img[i][j]=0
            for k in range(3):
                if bin_img[i+k-1][j] > 127:
                    out_img[i][j]=255
    return out_img


def all_erode(bin_img):
    out_img = np.zeros(shape=bin_img.shape, dtype=np.uint8) + 255
    h = bin_img.shape[0]
    w = bin_img.shape[1]
    B=[1,0,1,0,0,0,1,0,1]
    for i in range(1,h-1):
        for j in range(1,w-1):
            out_img[i][j]=0
            for m in range(3):
                for n in range(3):
                    if B[m*3+n] == 1:
                        continue
                    if bin_img[i+m-1][j+n-1] > 127:
                        out_img[i][j]=255
    return out_img

if __name__ == "__main__":
    img = cv2.imread("sample.bmp")
    # 灰度化
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    bin_img = get_binary_img(gray_img)
    out_img1 = horizon_erode(bin_img)
    out_img2 = vertical_erode(bin_img)
    out_img3 = all_erode(bin_img)
    cv2.imshow("img",img)
    cv2.imshow("bin", bin_img)
    cv2.imshow("out1", out_img1)
    cv2.imshow("out2", out_img2)
    cv2.imshow("out3", out_img3)
    cv2.waitKey(0)