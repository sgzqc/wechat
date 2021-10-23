import numpy as np
import os
import sys
import cv2


if __name__ == "__main__":
    img_file = "./images/bird_swarm.jpg"
    img = cv2.imread(img_file,cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    retval, bin_img = cv2.threshold(gray_img, 50, 1, cv2.THRESH_BINARY_INV)
    out_img = bin_img * 255

    m00 = m01 = m10 = m11 = m20 = m02 = m21 = m12 = 0
    height, width = bin_img.shape
    for y in range(height):
        for x in range(width):
            m00 += bin_img[y, x]
            m10 += x * bin_img[y, x]
            m01 += y * bin_img[y, x]
            m11 += x * y * bin_img[y, x]
            m20 += x * x * bin_img[y, x]
            m02 += y * y * bin_img[y, x]
            m21 += x * x * y * bin_img[y, x]
            m12 += x * y * y * bin_img[y, x]
    cx = m10/m00
    cy = m01/m00
    print('Centriod: ({0:.2f}, {1:.2f})'.format(cx, cy))

    mu00 = m00
    mu11 = m11 - cx * m01
    mu20 = m20 - cx * m10
    mu02 = m02 - cy * m01
    theta = 1 / 2 * np.arctan2(2 * mu11 / mu00, (mu20 - mu02) / mu00)
    print('Angle {0:.2f}'.format(theta * 180 / np.pi))

    # visual
    rho = 800
    dx_major = rho * np.cos(theta)
    dy_major = rho * np.sin(theta)
    dx_minor = 0.3 * rho * np.cos(theta - np.pi / 2)
    dy_minor = 0.3 * rho * np.sin(theta - np.pi / 2)
    # short
    short_axis=[(int(cx-dx_minor),int(cy-dy_minor)),(int(cx),int(cy)),(int(cx+dx_minor),int(cy+dy_minor))]
    for i in range(len(short_axis)-1):
        cv2.line(img,short_axis[i],short_axis[i+1],color=(255,0,0),thickness=2)
    for pt in short_axis:
        cv2.circle(img,pt,radius=5,color=(255,0,0),thickness=3,lineType=-1)

    # long
    long_axis = [(int(cx - dx_major), int(cy - dy_major)), (int(cx), int(cy)), (int(cx + dx_major), int(cy + dy_major))]
    for i in range(len(long_axis) - 1):
        cv2.line(img, long_axis[i], long_axis[i + 1], color=(0, 0, 255), thickness=2)
    for pt in long_axis:
        cv2.circle(img,pt,radius=5,color=(0,0,255),thickness=3,lineType=-1)

    cv2.circle(img, (int(cx),int(cy)), radius=5, color=(0, 255, 0), thickness=3, lineType=-1)

    cv2.imshow("img",img)
    cv2.imwrite("./results/task04/out5.jpg", img)
    cv2.waitKey(0)





