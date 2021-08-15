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
            bin_img[i][j] = 255 if img[i][j] < 255 else 0
    return bin_img


def label_from_seed(bin_img,visited,i,j,label,out_img):
    directs = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    seeds = [(i,j)]
    height = bin_img.shape[0]
    width = bin_img.shape[1]
    while len(seeds):
        seed = seeds.pop(0)
        i = seed[0]
        j = seed[1]
        if visited[i][j] == 0:
            visited[i][j] = 1
            out_img[i][j] = label

        # 以（i,j）为起点进行标记
        for direct in directs:
            cur_i = i + direct[0]
            cur_j = j + direct[1]
             # 非法
            if cur_i < 0 or cur_j < 0 or cur_i >= height or cur_j >= width:
                continue
             # 没有访问过
            if visited[cur_i][cur_j] == 0 and bin_img[cur_i][cur_j] == 255:
                visited[cur_i][cur_j] = 1
                out_img[cur_i][cur_j] = label
                seeds.append((cur_i,cur_j))




def label_region(bin_img,width,height):
    visited = np.zeros(shape=bin_img.shape,dtype=np.uint8)
    label_img = np.zeros(shape=bin_img.shape, dtype=np.uint8)
    label = 0
    for i in range(height):
        for j in range(width):
            if bin_img[i][j] == 255 and visited[i][j]==0 :
                # visit
                visited[i][j] = 1
                label += 1
                label_img[i][j] = label
                # label
                label_from_seed(bin_img, visited, i, j, label, label_img)

    return label_img,label


def get_region_area(label_img,label):
    count = { key: 0  for key in range(label + 1)}
    start_pt = {key:(0,0) for key in range(label + 1)}
    height = label_img.shape[0]
    width  = label_img.shape[1]
    for i in range(height):
        for j in range(width):
            key = label_img[i][j]
            count[key] += 1
            if count[key] == 1:
                start_pt[key] = (j,i)
    return count,start_pt


def draw_label_reslult(img,count,start_pt):
    draw = img.copy()
    for key in count.keys():
        if key > 0:
            pt = start_pt[key]
            x = pt[0]
            y = pt[1]
            if y < 20:
                y = 20
            cv2.putText(draw, str(key),(x,y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (128, 0, 128), 1)
    return draw


def draw_area_reslult(img,count,start_pt):
    draw = img.copy()
    for key in count.keys():
        if key > 0:
            pt = start_pt[key]
            x = pt[0]
            y = pt[1]
            area = count[key]
            if y < 20:
                y = 20
            cv2.putText(draw, str(area),(x,y), cv2.FONT_HERSHEY_COMPLEX, 0.8, (128, 0, 128), 1)
    return draw




if __name__ == "__main__":
    file_name = "./test.bmp"
    img = cv2.imread(file_name)
    h = img.shape[0]
    w = img.shape[1]
    print(h,w)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bin_img = get_binary_img(gray_img)
    # 标记
    label_img,label = label_region(bin_img,w,h)
    count, start_pt =  get_region_area(label_img, label)


    out_label = draw_label_reslult(img, count, start_pt)
    out_area = draw_area_reslult(img, count, start_pt)

    merge_img = cv2.hconcat([img, out_label])
    cv2.imwrite("./20210815/merge_label.jpg",merge_img)

    merge_img = cv2.hconcat([img, out_area])
    cv2.imwrite("./20210815/merge_area.jpg", merge_img)

    merge_img = cv2.hconcat([img, out_label,out_area])
    cv2.imwrite("./20210815/merge_all2.jpg", merge_img)

    cv2.imshow("label",out_label)
    cv2.imshow("area", out_area)
    cv2.waitKey(0)








