import numpy as np
import argparse
import cv2


def grab_contours(cnts):
    # if the length the contours tuple returned by cv2.findContours
    # is '2' then we are using either OpenCV v2.4, v4-beta, or
    # v4-official
    if len(cnts) == 2:
        cnts = cnts[0]

    # if the length of the contours tuple is '3' then we are using
    # either OpenCV v3, v4-pre, or v4-alpha
    elif len(cnts) == 3:
        cnts = cnts[1]

    return cnts


def sort_contours(cnts, method='left-to-right'):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0
    # handle if sort in reverse
    if method == 'right-to-left' or method == 'bottom-to-top':
        reverse = True
    # handle if sort against y rather than x of the bounding box
    if method == 'bottom-to-top' or method == 'top-to-bottom':
        i = 1

    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b: b[1][i], reverse=reverse))
    return (cnts, boundingBoxes)


def draw_contour(image, c, i):
    M = cv2.moments(c)
    cX = int(M['m10'] / M['m00'])
    cY = int(M['m01'] / M['m00'])
    cv2.putText(image, '#{}'.format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    return image


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=False, help='path to the image',default='./image/lego_blocks_1.png')
    ap.add_argument('-m', '--method', required=False, help='Sorting method',default='left-to-right')
    args = vars(ap.parse_args())

    image = cv2.imread(args['image'])
    accumEdged = np.zeros(image.shape[:2], dtype='uint8')
    for chan in cv2.split(image):
        chan = cv2.medianBlur(chan, 11)
        edged = cv2.Canny(chan, 50, 200)
        accumEdged = cv2.bitwise_or(accumEdged, edged)


    # find contours and keep the largest ones
    cnts = cv2.findContours(accumEdged.copy(), cv2.RETR_EXTERNAL,  cv2.CHAIN_APPROX_SIMPLE)
    cnts = grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    orig = image.copy()
    # unsorted
    for (i, c) in enumerate(cnts):
        orig = draw_contour(orig, c, i)
    cv2.imshow('Unsorted', orig)

    # sorted
    (cnts, boundingboxes) = sort_contours(cnts, method=args['method'])
    image2 = image.copy()
    for (i, c) in enumerate(cnts):
        image2 = draw_contour(image2, c, i)
    cv2.imshow('Sorted', image2)

    out = cv2.hconcat([image,orig,image2])
    cv2.imwrite("./result/out1.jpg",out)
    cv2.waitKey(0)




