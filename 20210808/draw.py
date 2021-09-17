import os
import sys
import cv2
import numpy as np


def get_binary_img(img):
    # gray img to bin image
    bin_img = np.zeros(shape=(img.shape), dtype=np.uint8)
    h = img.shape[0]
    w = img.shape[1]
    for i in range(h):
        for j in range(w):
            bin_img[i][j] = 255 if img[i][j] > 127 else 0
    return bin_img


def get_contour(bin_img):
    # get contour
    contour_img = np.zeros(shape=(bin_img.shape),dtype=np.uint8)
    contour_img += 255
    h = bin_img.shape[0]
    w = bin_img.shape[1]
    for i in range(1,h-1):
        for j in range(1,w-1):
            if(bin_img[i][j]==0):
                contour_img[i][j] = 0
                sum = 0
                sum += bin_img[i - 1][j + 1]
                sum += bin_img[i][j + 1]
                sum += bin_img[i + 1][j + 1]
                sum += bin_img[i - 1][j]
                sum += bin_img[i + 1][j]
                sum += bin_img[i - 1][j - 1]
                sum += bin_img[i][j - 1]
                sum += bin_img[i + 1][j - 1]
                if sum ==  0:
                    contour_img[i][j] = 255

    return contour_img


if __name__ == "__main__":
    img_name = "./20210808/sample3.png"
    img = cv2.imread(img_name)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bin_img = get_binary_img(gray_img)
    contour_img = get_contour(bin_img)

    cv2.imshow("src", img)
    cv2.imshow("contour",contour_img)
    cv2.waitKey(0)
