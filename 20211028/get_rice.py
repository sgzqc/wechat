import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from skimage.color import label2rgb
import seaborn # pylint: disable=unused-import
import cv2

import moments

def plot_image(image, fig_num, name=None, colormap='gray', write_file=None):
  """Plot image"""
  fig = plt.figure(fig_num)
  plt.imshow(image, cmap=colormap, interpolation='none')
  if name is not None:
    plt.title(name)
  plt.xticks([]), plt.yticks([])
  plt.tight_layout()
  if write_file:
    fig.savefig(write_file, bbox_inches='tight', pad_inches=0)
  fig_num += 1
  return fig_num

def plot_line_and_histogram(ordinate,
                            abscissa=None,
                            fig_num=0,
                            title='Plot and histogram',
                            label='Value',
                            num_bins=None,
                            bin_range=None,
                            normed=True,
                            marker='',
                            linestyle='.',
                            linewidth=1.0):
  """2D line plot and histogram"""

  if abscissa is None:
    abscissa = np.array(list(range(len(ordinate))))
  if num_bins is None:
    num_bins = 10
  if bin_range is None:
    bin_range = [np.min(ordinate), np.max(ordinate)]

  #fig = plt.figure(fig_num, figsize=(8, 5))
  fig = plt.figure(fig_num)
  fig.suptitle(title)
  #gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1], width_ratios=[1, 1])
  gs = gridspec.GridSpec(3, 1)
  ax0 = fig.add_subplot(gs[0:2, :])
  ax0.plot(abscissa, ordinate, marker=marker, linestyle=linestyle,
           linewidth=linewidth)
  ax0.set_ylabel(label)
  ax1 = fig.add_subplot(gs[2, :])
  ax1.hist(ordinate, bins=num_bins, range=bin_range)
  ax1.set_xlabel(label)

  gs.tight_layout(fig)
  fig_num += 1

  return fig_num

def main():
  """Connected components"""
  # Configurations
  fig_num = 0
  os.makedirs('results/task02', exist_ok=True)
  # Step 1: Read image
  image_file = './images/rice.png'
  image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
  fig_num = plot_image(image, fig_num,
                       write_file='results/task02/original_image.png')

  # Step 2: Use morphological opening to estimate the background
  selem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31))
  background = cv2.morphologyEx(image, cv2.MORPH_OPEN, selem)
  fig_num = plot_image(background, fig_num,
                       write_file='results/task02/background_image.png')

  # Step 3: Subtract the background image from the original image
  foreground = cv2.subtract(image, background)
  fig_num = plot_image(foreground, fig_num,
                       write_file='results/task02/foreground_image.png')

  # Step 4: Increase the image contrast
  # Here, we can implement our own, or use the built in global histogram equalization
  contrasted = cv2.equalizeHist(foreground)
  # Or we can try out the Contrast Limited Adaptive Histogram Equalization
  #clahe = cv2.createCLAHE()
  #contrasted = clahe.apply(foreground)
  fig_num = plot_image(contrasted, fig_num,
                       write_file='results/task02/histeq_image.png')
  # As is evident, none seems to work very well

  # Step 5: Threshold the image
  # The contrast adjustments seems to only make things worse (way to much
  # contrast emphasis on the background noise), so we threshold the foreground
  # image directly.
  thresh_otsu, binary_image = cv2.threshold(foreground.astype(np.uint8), 0, 255,
                                            cv2.THRESH_BINARY+cv2.THRESH_OTSU)

  print('Threshold: ', thresh_otsu)
  fig_num = plot_image(binary_image, fig_num,
                       write_file='results/task02/thresholded_image.png')

  # Step 6: Label objects in the image
  _, label_image = cv2.connectedComponents(binary_image, connectivity=4)

  # Step 7: Examine the label image
  # First, we select the grain labeled 43, and finds its contour
  single_grain_full = (label_image == 43)
  cnt_list, _ = cv2.findContours(single_grain_full.astype(np.uint8),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_NONE)

  # As there is only one contour, we select it, and use it to compute a
  # bounding box around the grain
  grain_contour = cnt_list[0]
  y_start, x_start, dy, dx = cv2.boundingRect(grain_contour)
  grain_min_bbox = label_image[x_start:x_start+dx, y_start:y_start+dy].astype(np.uint8)

  # grain_min_bbox is the minimal bounding box around the grain, so we pad it a
  # bit before we display it.
  grain_bbox = cv2.copyMakeBorder(grain_min_bbox, 10, 10, 10, 10,
                                  cv2.BORDER_CONSTANT, value=0)
  fig_num = plot_image(grain_bbox, fig_num,
                       write_file='results/task02/grain_43.png')

  # Step 8: Display the label image
  fig_num = plot_image(label2rgb(label_image), fig_num,
                       write_file='results/task02/rgb_label_image.png')
  fig_num = plot_image(label_image, fig_num, colormap='magma',
                       write_file='results/task02/gl_label_image.png')

  # Step 9 (and 12): Measure centroid, area (and orientation) of object We compute all properties using their moments.
  # moments from interior of objects (own implementation)
  moment_dict = moments.get_moment_list(label_image)
  print(moment_dict[1])



  # Superimplose labels, centriods and orientation over this image
  fig = plt.figure(fig_num)
  plt.imshow(image, cmap='gray', interpolation='none')
  plt.xticks([]), plt.yticks([])
  plt.tight_layout()
  obj_properties = {}
  for ind, obj_moments in moment_dict.items():
    if obj_moments['m00'] > 0:
      # Area
      area = obj_moments['m00']
      theta = obj_moments['theta']
      cx = int(obj_moments['m10'] / obj_moments['m00'])
      cy = int(obj_moments['m01'] / obj_moments['m00'])
      rho = 10
      dx = rho*np.cos(theta)
      dy = rho*np.sin(theta)
      if abs(theta*180/np.pi) <= 20:
        plt.plot([cx-dx, cx, cx+dx], [cy-dy, cy, cy+dy], 'go-')
      else:
        plt.plot([cx-dx, cx, cx+dx], [cy-dy, cy, cy+dy], 'bo-')
      plt.text(cx, cy, str(ind), color='red', fontsize=14)
      # Store properties
      props = {}
      props['area'] = area
      props['cx'] = cx
      props['cy'] = cy
      props['theta'] = theta*180/np.pi
      obj_properties[ind] = props
  print(obj_properties[1])

  axes = plt.gca()
  axes.set_xlim([0, label_image.shape[0]])
  axes.set_ylim([label_image.shape[1], 0])
  fig.savefig('results/task02/marked_image.png', bbox_inches='tight', pad_inches=0)
  fig_num += 1

  areas = []
  orientations = []
  print('Object      Area Orientation Centroid')
  for ind, props in obj_properties.items():
    areas.append(props['area'])
    orientations.append(props['theta'])
    print('{0:>6} {1:>9,.0f} {2:>11,.2f} ({3:>3}, {4:>3})'.format(ind,
                                                                  props['area'],
                                                                  props['theta'],
                                                                  props['cx'],
                                                                  props['cy']))

  fig_num = plot_line_and_histogram(areas, title='Areas', marker='*',
                                    linestyle='', fig_num=fig_num, num_bins=30,
                                    normed=False, label='Area (pixels)')
  fig_num = plot_line_and_histogram(orientations, title='Orientations',
                                    marker='*', linestyle='',
                                    fig_num=fig_num, num_bins=30,
                                    normed=False, label='Angle (degrees)')

  # Index + 1 because of zero indexing in list, while the object labels are
  # enumerated from 1 (since label 0 is reserved to backround).
  print('Grain {} has the largest area of {} pixels'.format(np.argmax(areas)+1,
                                                            np.max(areas)))
  print('Mean area: {0:.2f}'.format(np.mean(areas)))

  plt.show()

if __name__ == "__main__":
  main()
