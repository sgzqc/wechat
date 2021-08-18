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


def get_vertical_project(img):
    h, w  = img.shape
    project_img = np.zeros(shape=(img.shape), dtype=np.uint8) + 255
    for j in range(w):
        num = 0
        for i in range(h):
            if img[i][j] == 0:
                num+=1
        for k in range(num):
            project_img[h-1-k][j] = 0
    return project_img


def get_horizon_project(img):
    h, w  = img.shape
    project_img = np.zeros(shape=(img.shape), dtype=np.uint8) + 255
    for i in range(h):
        num = 0
        for j in range(w):
            if img[i][j] == 0:
                num+=1
        for k in range(num):
            project_img[i][k] = 0
    return project_img



def get_vertical_project_update(img):
    h, w  = img.shape
    project_img = np.zeros(shape=(img.shape), dtype=np.uint8) + 255
    start = end = 0
    find_start = find_end = 0
    pre_num = 0
    for j in range(w):
        num = 0
        for i in range(h):
            if img[i][j] == 0:
                num+=1
        for k in range(num):
            project_img[h-1-k][j] = 0
        if not find_start and pre_num==0 and num != pre_num :
            start = j
            find_start = 1
        if not find_end and num == 0 and num != pre_num:
            end = j
            find_end = 1
        pre_num = num
    return project_img,start,end


def get_horizon_project_update(img):
    h, w  = img.shape
    project_img = np.zeros(shape=(img.shape), dtype=np.uint8) + 255
    start = end = 0
    find_start = find_end = 0
    pre_num = 0
    for i in range(h):
        num = 0
        for j in range(w):
            if img[i][j] == 0:
                num+=1
        for k in range(num):
            project_img[i][k] = 0
        if not find_start and pre_num==0 and num != pre_num :
            start = i
            find_start = 1
        if not find_end and num == 0 and num != pre_num:
            end = i
            find_end = 1
        pre_num = num
    return project_img,start,end


def test1():
    file_name = "./sample/test2.png"
    img = cv2.imread(file_name)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 调用
    bin_img = get_binary_img(gray_img)
    horizon_img = get_horizon_project(bin_img)
    vertical_img = get_vertical_project(bin_img)
    # 显示
    cv2.imshow("bin", bin_img)
    cv2.imshow("horizon", horizon_img)
    cv2.imshow("vertical", vertical_img)
    cv2.waitKey(0)


def draw_horizon(img,start_i,end_i):
    out_img = img.copy()
    h,w,c = img.shape
    cv2.line(out_img, (0, start_i),( h- 1, start_i),color=(0,0,255),  thickness=2)
    cv2.line(out_img, (0, end_i),  (h - 1, end_i), color=(0, 0, 255), thickness=2)
    return out_img


def draw_vertical(img,start_j,end_j):
    out_img = img.copy()
    h,w,c = img.shape
    cv2.line(out_img, (start_j, 0), (start_j, h - 1), color=(0, 0, 255), thickness=2)
    cv2.line(out_img, (end_j, 0), (end_j, h - 1), color=(0, 0, 255), thickness=2)
    return out_img


def test2():
    file_name = "/media/zhaoqichao/92A8C550A8C5340F/wechat/20210818/test2.png"
    img = cv2.imread(file_name)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 调用
    bin_img = get_binary_img(gray_img)
    horizon_img,start_i,end_i = get_horizon_project_update(bin_img)
    vertical_img,start_j,end_j = get_vertical_project_update(bin_img)
    # 画图
    show_img = img.copy()
    cv2.rectangle(show_img, (start_j, start_i), (end_j, end_i), color=(0, 0, 255), thickness=2)
    # 展示
    cv2.imshow("bin", bin_img)
    cv2.imshow("horizon", horizon_img)
    cv2.imshow("vertical", vertical_img)

    # 画图
    merge_bin = cv2.merge([bin_img, bin_img, bin_img])
    merge_horizon = cv2.merge([horizon_img, horizon_img, horizon_img])
    merge_vertical = cv2.merge([vertical_img, vertical_img, vertical_img])

    out_bin_horizon = draw_horizon(merge_bin,start_i,end_i)
    out_horizon = draw_horizon(merge_horizon, start_i, end_i)

    out_bin_vertical = draw_vertical(merge_bin, start_j, end_j)
    out_vertical = draw_vertical(merge_vertical, start_j, end_j)

    cv2.imshow("res", show_img)
    cv2.imshow("out_bin_horizon", out_bin_horizon)
    cv2.imshow("out_horizon", out_horizon)
    cv2.imshow("out_bin_vertical", out_bin_vertical)
    cv2.imshow("out_vertical", out_vertical)

    cv2.imwrite("out_bin_horizon.jpg", out_bin_horizon)
    cv2.imwrite("out_horizon.jpg", out_horizon)
    cv2.imwrite("out_bin_vertical.jpg", out_bin_vertical)
    cv2.imwrite("out_vertical.jpg", out_vertical)
    cv2.imwrite("res.jpg", show_img)

    out5 = cv2.hconcat([merge_bin,out_horizon, out_vertical,show_img])
    cv2.imwrite("out5.jpg", out5)
    cv2.waitKey(0)


if __name__ == "__main__":
    #test1()
    test2()
