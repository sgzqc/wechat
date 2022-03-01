import os
import sys
import cv2
import numpy as np

if __name__ == "__main__":
    im = cv2.imread("./ladder.png")
    gray_img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    merge = cv2.merge([gray_img,gray_img,gray_img])
    out_img = cv2.hconcat([im,merge])
    cv2.imwrite("out1.jpg",out_img)

    canny = cv2.Canny(gray_img, 30, 150)
    cv2.imwrite("out2.jpg", canny)

    lines = cv2.HoughLines(canny, 1, np.pi / 180, 180)
    lines1 = lines[:, 0, :]
    for rho, theta in lines1[:]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 3000 * (-b))
        y1 = int(y0 + 3000 * (a))
        x2 = int(x0 - 3000 * (-b))
        y2 = int(y0 - 3000 * (a))
        cv2.line(im, (x1, y1), (x2, y2), (0, 0, 255), 2)

    cv2.imwrite("out3.jpg", im)

    cv2.imshow("res",im)
    cv2.waitKey(0)