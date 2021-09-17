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



if __name__ == "__main__":
    img_name = "./sample2.jpg"
    img = cv2.imread(img_name)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 调用
    bin_img = get_binary_img(gray_img)
    h = bin_img.shape[0]
    w = bin_img.shape[1]
   # 8 邻域
    directs = [(-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1),(-1,1),(-1,0)]
    out_img = np.zeros(shape=(bin_img.shape), dtype=np.uint8)
    visited = np.zeros(shape=(bin_img.shape), dtype=np.uint8)
    draw_img = img.copy()
    # 选择初始3个种子点
    seeds = [(176,255),(229,405),(347,165)]
    for seed in seeds:
        x = seed[0]
        y = seed[1]
        out_img[y][x] = 255

        offset = 5
        color = (128,0,128)  #(0,255,255)
        cv2.line(draw_img, (x - offset, y), (x + offset, y), color, 2, 1)
        cv2.line(draw_img, (x , y - offset), (x, y+offset), color, 2, 1)

    while len(seeds):
        seed = seeds.pop(0)
        x = seed[0]
        y = seed[1]
        # visit point (x,y)
        visited[y][x] = 1

        for direct in directs:
            cur_x = x + direct[0]
            cur_y = y + direct[1]

            if cur_x <0 or cur_y<0 or cur_x >= w or cur_y >=h :
                continue

            if (not visited[cur_y][cur_x]) and (bin_img[cur_y][cur_x]==bin_img[y][x]) :
                out_img[cur_y][cur_x] = 255
                visited[cur_y][cur_x] = 1
                seeds.append((cur_x,cur_y))

    bake_img = img.copy()
    for i in range(h):
        for j in range(w):
            if out_img[i][j] != 255:
                bake_img[i][j][0] = 0
                bake_img[i][j][1] = 0
                bake_img[i][j][2] = 0


    merge = cv2.merge([out_img,out_img,out_img])
    res = cv2.hconcat( [draw_img,merge,bake_img])
    res2 = cv2.hconcat([draw_img, bake_img])
    cv2.imwrite("merge.jpg", res)
    cv2.imwrite("merge2.jpg", res2)
    cv2.imshow("lala",res)
    cv2.waitKey(0)