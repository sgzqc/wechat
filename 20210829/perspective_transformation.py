import cv2
import numpy as np


def test():
    img = cv2.imread("image/sample.jpg")
    h, w, c = img.shape  # h=240  w=320
    print(h, w, c)
    src_list = [(61, 70), (151, 217), (269, 143), (160, 29)]
    for i, pt in enumerate(src_list):
        cv2.circle(img, pt, 5, (0, 0, 255), -1)
        #cv2.putText(img,str(i+1),(pt[0]+5,pt[1]+10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    pts1 = np.float32(src_list)

    pts2 = np.float32([[0, 0], [0, w - 2], [h - 2, w - 2], [h - 2, 0]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (h, w))
    cv2.imshow("Image", img)
    cv2.imshow("Perspective transformation", result)
    cv2.waitKey(0)



def draw_merge():
    img1 = cv2.imread("draw_digital.jpg")
    h1, w1, c = img1.shape  # h=240  w=320

    img2 = cv2.imread("draw_result.jpg")
    h2, w2, c = img2.shape  # h=320  w=240

    dst_img = np.zeros((h2,w1+w2,c),np.uint8)
    dst_img[0:h1,0:w1,:] = img1
    dst_img[0:h2,w1:,:] = img2
    cv2.imshow("test",dst_img)
    cv2.imwrite("merge.jpg", dst_img)
    cv2.waitKey(0)


def test3():
    src_img = cv2.imread("image/logo.jpg")
    h, w, c = src_img.shape  # h=240  w=320
    print(h, w, c)

    src_list = [(0, 0), (0, h-1), (w-1, h-1), (w-1, 0)]
    pts1 = np.float32(src_list)
    #
    pts2 = np.float32([[173, 108], [178, 458], [375, 455], [373, 113]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    logo = cv2.imread("image/sample2.jpg")
    h2, w2, c = logo.shape
    result = cv2.warpPerspective(src_img, matrix, (w2, h2))
    gary_image = cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    ret,bin_img = cv2.threshold(gary_image,5,250,cv2.THRESH_BINARY)

    dilate = cv2.dilate(bin_img,None,iterations=1)
    logo[dilate>0] = result[dilate>0]

    cv2.imshow("src", src_img)
    cv2.imshow("out", logo)
    cv2.waitKey(0)





if __name__ == "__main__":
    test()
    test3()



