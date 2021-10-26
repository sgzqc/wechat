import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage import morphology
from scipy.ndimage.morphology import binary_fill_holes


def main():
  image_file = './images/pillsetc.png'
  # Step 1: Read image
  bgr_image = cv2.imread(image_file,cv2.IMREAD_COLOR)
  # Step 2: Threshold the image
  gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
  threshold, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
  print('Graylevel threshold computed with otsu: ', threshold)

  # Step 3: Remove the noise
  # Remove objects containing fewer than 30 pixels (both gives essentially the same output)
  rmnoise_image = morphology.remove_small_objects(thresh_image.astype(bool), min_size=30)

  # Fill a gap in the cap of the pen
  fillcap_image = morphology.binary_closing(rmnoise_image, selem=morphology.disk(2))

  # Fill holes
  clean_image = binary_fill_holes(fillcap_image)

  # Step 4: Find boundaries
  contours, _ = cv2.findContours(clean_image.astype(np.uint8), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
  h,w = clean_image.shape
  obj_image = np.zeros(shape=(h,w,3),dtype=np.uint8)
  color_list=[(94,17,43),(128,31,113),(121,54,180),(118,173,253),(190,251,250),(93,96,239)]
  for ind, cnt in enumerate(contours):
    cv2.drawContours(obj_image, [cnt], 0,color_list[ind], -1)


  # Step 5: Determine which objects are round
  # For a circle, the following relationship will hold
  #
  #         4 * pi * Area / Circumference^2 = 1
  #
  # Therefore, we use the metric alpha = 4*pi*Area/Perimeter^2 to determine how round the
  # shape is, the closer it is to one, the rounder it is. Mark the center of all
  # objects with alpha > round_thresh
  round_thresh = 0.9
  height, width,channel = obj_image.shape
  print('Object      Area Perimeter Roundness')
  for ind, contour in enumerate(contours):
    # Compute a simple estimate of the object perimeter
    # contour is a list of N coordinate points (x_i, y_i), and the perimeter is computed as
    # perimeter = sum_{i=0}^{N-2} ( sqrt( (x_{i+1} - x_i)^2 + (y_{i+1} - y_i)^2 ))
    delta_squared = np.diff(contour, axis=0)*np.diff(contour, axis=0)
    perimeter = np.sum(np.sqrt(np.sum(delta_squared, axis=1)))
    # or use the built in arcLength() (both arcLength() and contourArea() are
    # based on Freeman chain codes).
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    alpha = 4*np.pi*area/(perimeter**2)
    print('{0:>6} {1:>9,.0f} {2:>9,.2f} {3:>9,.3f}'.format(ind, area, perimeter, alpha))
    # Compute moments in order to find the centroid of objects
    moments = cv2.moments(contour)
    cx = int(moments['m10'] / moments['m00'])
    cy = int(moments['m01'] / moments['m00'])

    cv2.putText(obj_image,str(ind),(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,color=(0,128,0),thickness=2)

    # Plot a red circle on the centroid of the round objects
    if alpha > round_thresh:
       cv2.circle(obj_image,(cx,cy),2,color=(0,0,255),thickness=2)

  cv2.imshow("result",obj_image)
  cv2.waitKey(0)
  cv2.imwrite('results/marked_image.png', obj_image )




if __name__ == "__main__":
  main()
