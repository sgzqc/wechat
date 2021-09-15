import os
import sys
import math
import cv2
import numpy as np

config = {
    "cell_num":4,
    "whether_crop_image_height": False,
    "whether_with_gap": True,
    "gap_width":3
}


def cut_without_gap(img):
    w_count = config['cell_num']
    src_height = img.shape[0]
    src_width = img.shape[1]
    sub_length = int(src_width / w_count)
    new_width = sub_length * w_count

    if config['whether_crop_image_height']:
        h_count = int(src_height / sub_length)
    else:
        h_count = math.ceil(src_height / sub_length)

    new_height = sub_length * h_count

    img_t = np.zeros(shape=(new_height,new_width,3),dtype=np.uint8) + 255

    if config['whether_crop_image_height']:
        img_t = img[:new_height,:new_width,:]
    else:
        img_t[:src_height, :new_width, :] = img[:src_height, :new_width, :]

    for x_i in range(1, w_count):
        cv2.line(img_t,(x_i*sub_length,0),(x_i*sub_length,new_height-1),color=(205,205,74),thickness=1)
    for y_i in range(1, h_count):
        cv2.line(img_t, (0,y_i*sub_length), (new_width-1,y_i*sub_length), color=(205,205,74), thickness=1)

    return img_t


def cut_with_gap(img):
    w_count = config['cell_num']
    src_height = img.shape[0]
    src_width = img.shape[1]

    sub_length = int(src_width / w_count)
    gap_length = int(config["gap_width"])
    new_width = sub_length * w_count + gap_length * (w_count -1)

    if config['whether_crop_image_height']:
        h_count = int( (src_height + gap_length) / (sub_length+gap_length))
    else:
        h_count = math.ceil((src_height + gap_length) / (sub_length+gap_length))

    new_height = sub_length * h_count + gap_length * (h_count-1)
    img_t = np.zeros(shape=(new_height,new_width,3),dtype=np.uint8) + 255

    if config['whether_crop_image_height']:
        for i in range(h_count):  # 3
            for j in range(w_count): # 7
                begin_x = sub_length * j
                begin_y = sub_length * i
                src_x = gap_length * j + begin_x
                src_y = gap_length * i + begin_y
                img_t[src_y:src_y+sub_length,src_x:src_x + sub_length,:] = img[begin_y:begin_y + sub_length,begin_x:begin_x + sub_length,  :]
    else:
        for i in range(h_count):
            for j in range(w_count):
                begin_x = sub_length * j
                begin_y = sub_length * i
                src_x = gap_length * j + begin_x
                src_y = gap_length * i + begin_y
                if i<h_count-1:
                    img_t[src_y:src_y+sub_length,src_x:src_x + sub_length,:] = img[begin_y:begin_y + sub_length,begin_x:begin_x + sub_length,  :]
                else:
                    diff_height = src_height - sub_length * (h_count-1)
                    img_t[src_y:src_y + diff_height, src_x:src_x + sub_length, :] = img[begin_y:begin_y + diff_height,
                                                                                   begin_x:begin_x + sub_length, :]
    return img_t


if __name__ == "__main__":
    #file_name = "./test.jpeg"
    file_name = './xiaohua.jpeg'
    img = cv2.imread(file_name)
    if config["whether_with_gap"]:
        out_img = cut_with_gap(img)
    else:
        out_img = cut_without_gap(img)

    cv2.imwrite("result4.jpg",out_img)
    cv2.imshow("test",out_img)
    cv2.waitKey(0)