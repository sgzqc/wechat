import os
import cv2
import numpy as np


if __name__ == "__main__":
    img_file = "./sample.jpeg"
    img1 = cv2.imread(img_file)
    img  = cv2.resize(img1,(640,400))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval, bin_img = cv2.threshold(gray_img, 120, 255, cv2.THRESH_BINARY )
    img_median = cv2.medianBlur(bin_img, 3)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    erosion_img = cv2.erode(img_median, kernel, iterations=2)

    dilatation_type = cv2.MORPH_ELLIPSE
    dilatation_size = 1
    element = cv2.getStructuringElement(dilatation_type, (2 * dilatation_size + 1, 2 * dilatation_size + 1),
                                       (dilatation_size, dilatation_size))
    dilate_img = cv2.dilate(erosion_img, element,iterations=3)


    contours, hierarchy = cv2.findContours(dilate_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out_img = img.copy()
    for contour in contours:
        area = cv2.contourArea(contour)
        k = cv2.isContourConvex(contour)
        if  area>150:
            cv2.drawContours(img, [contour, ], -1, (255, 0, 255), 2)  # red

    for contour in contours:
        cv2.drawContours(out_img, [contour, ], -1, (0 ,0, 255), 2)  # red


    cv2.imshow("bin",bin_img)
    cv2.imshow("median", img_median)
    cv2.imshow("erode", erosion_img)
    cv2.imshow("dilate", dilate_img)
    cv2.imshow("result", img)
    cv2.imshow("result2",out_img)

    cv2.waitKey(0)
