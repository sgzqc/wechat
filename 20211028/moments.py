"""
A verbose implementation of how to compute some moments of objects, and
properties derived thereof.

For an image with values f[x, y], we have the following:

Moments

  m_pq = sum_x sum_y x^p * y^q f[x, y]

Central moments

  mu_pq = sum_x sum_y (x - cx)^p * (y - cy)^p f[x, y]

Normalized central moments

  nu_pq = mu_pq / (mu_00^((p+q)/2 + 1), for p+q >= 2

Where

  Area of a binary image:
    a = m_00
  Centroids (cx, cy):
    cx = m_10 / m_00
    cy = m_01 / m_00
  Covariance matrix:
    cov = [[mu_20, mu_11], [mu_11, mu_02]] / mu_00
  Orientation (angle of the major axis (largest eigenvector))
    theta = 1/2 * arctan( 2*mu_11 / (mu_20 - mu_02); if mu_20 != mu_02
    theta = 1/2 * np.pi / 2; if mu_20 == mu_02
"""

# pylint: disable=bad-indentation

import numpy as np
import cv2

def get_moment_list(label_image):
  """
  Compute moments for each foreground object found in an image, and return them.

  Args:
    label_mage: An image where the pixels from the same connected region share
                a label. If it is not already labeled, we label it in the start
                of the routine. It is assumed that the background is labeled 0,
                and foreground >0. An object is defined to be a set of equal pixel
                intensities, which are also serving as the label.
  Returns:
    moment_list: List of object moments and properties.
  """

  if not label_image.dtype is 'uint8':
    label_image = label_image.astype('uint8')
  if not len(np.unique(label_image)) > 2:
    _, label_image = cv2.connectedComponents(label_image)

  height, width = label_image.shape

  labels = np.unique(label_image)[1:] # We descard the background

  # Naive implementation. Traverse all objects, and then compute the moments by
  # traversing the whole image.
  moment_list = {}
  for obj_label in labels:
    # Compute raw moments
    moment = {}
    moment['m00'] = 0.0
    moment['m01'] = 0.0
    moment['m10'] = 0.0
    moment['m11'] = 0.0
    moment['m02'] = 0.0
    moment['m12'] = 0.0
    moment['m21'] = 0.0
    moment['m20'] = 0.0
    moment['m22'] = 0.0
    # Traverse the image (note the ordinary cartesian x,y coordinate convention)
    for y in range(height):
      for x in range(width):
        if label_image[y, x] == obj_label:
          # Assume label_image[y,x] = 1, st. area is in pixels^2 units
          moment['m00'] += 1
          moment['m10'] += x
          moment['m01'] += y
          moment['m11'] += x*y
          moment['m20'] += x*x
          moment['m02'] += y*y
          moment['m12'] += x*y*y
          moment['m21'] += x*x*y
          moment['m22'] += x*x*y*y

    if moment['m00'] > 0:

      # Centroid
      cx = moment['m10'] / moment['m00']
      cy = moment['m01'] / moment['m00']

      # Central moments
      moment['mu00'] = moment['m00']
      moment['mu01'] = 0
      moment['mu10'] = 0
      moment['mu11'] = moment['m11'] - cx*moment['m01']
      moment['mu20'] = moment['m20'] - cx*moment['m10']
      moment['mu02'] = moment['m02'] - cy*moment['m01']
      moment['mu21'] = moment['m21'] - 2*cx*moment['m11'] - cy*moment['m20'] + 2*cx*cx*moment['m01']
      moment['mu12'] = moment['m12'] - 2*cy*moment['m11'] - cx*moment['m02'] + 2*cy*cy*moment['m10']

      # Normalized central moments
      moment['nu00'] = 1
      moment['nu01'] = 0
      moment['nu10'] = 0
      moment['nu11'] = moment['mu11'] / (moment['mu00']**(2))
      moment['nu02'] = moment['mu02'] / (moment['mu00']**(2))
      moment['nu20'] = moment['mu20'] / (moment['mu00']**(2))
      moment['nu12'] = moment['mu12'] / (moment['mu00']**(2.5))
      moment['nu21'] = moment['mu21'] / (moment['mu00']**(2.5))

      # Misc properties
      moment['area'] = moment['m00']
      moment['cx'] = cx
      moment['cy'] = cy
      moment['cov_mat'] = np.array([[moment['mu20'], moment['mu11']],
                                    [moment['mu11'], moment['mu02']]])/moment['mu00']
      if moment['mu20'] == moment['mu02']:
          moment['theta'] = 1/2 * np.pi / 2
      else:
          moment['theta'] = 1/2 * np.arctan2(2*moment['mu11']/moment['mu00'],
                                             (moment['mu20'] - moment['mu02'])/moment['mu00'])

      moment_list[obj_label] = moment

  return moment_list
