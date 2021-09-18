import os
import cv2
import numpy as np


def get_binary_img(img):
    # gray img to bin image
    bin_img = np.zeros(shape=(img.shape), dtype=np.uint8)
    h = img.shape[0]
    w = img.shape[1]
    for i in range(h):
        for j in range(w):
            bin_img[i][j] = 255 if img[i][j] > 200 else 0
    return bin_img


# 从左上角查找开始
def get_left_up_start_pt(bin_img):
    h = bin_img.shape[0]
    w = bin_img.shape[1]
    find = 0
    start_i = 0
    start_j = 0
    for i in range(h):
        for j in range(w):
            if bin_img[i][j] == 0:
                find = 1
                start_i = i
                start_j = j
                break
    return find,start_i,start_j


def trace_contour(bin_img,find,start_i,start_j):
    contour_img = np.zeros(shape=(bin_img.shape), dtype=np.uint8)
    contour_img += 255
    if find:
        contour_img[start_i][start_j] = 0

    Direct = [(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0)]
    BeginDirect = 0
    findstart = 0
    cur_i = start_i
    cur_j = start_j

    while findstart==0 :
        findpoint = 0
        while findpoint==0:
            i = cur_i + Direct[BeginDirect][1]
            j = cur_j + Direct[BeginDirect][0]
            pixel = bin_img[i][j]
            if pixel==0:
                findpoint = 1
                cur_i = i
                cur_j = j
                if cur_i ==start_i and cur_j == start_j:
                    findstart = 1

                contour_img[cur_i][cur_j] = 0

                BeginDirect-=1
                if BeginDirect == -1:
                    BeginDirect = 7
                BeginDirect-=1
                if BeginDirect == -1:
                    BeginDirect = 7
            else:
                BeginDirect += 1
                if BeginDirect == 8:
                    BeginDirect = 0

    return contour_img


if __name__ == "__main__":
    img_name = "./sample.bmp"
    img = cv2.imread(img_name)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 调用
    bin_img = get_binary_img(gray_img)
    # 调用
    find, start_i, start_j = get_left_up_start_pt(bin_img)
    contour_img = trace_contour(bin_img, find, start_i, start_j)
    cv2.imshow("src", img)
    cv2.imshow("result",contour_img)
    cv2.waitKey(0)
