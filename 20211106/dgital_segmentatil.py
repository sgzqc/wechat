import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage.color import label2rgb


def plot_image(image, name, fig_num, colormap='gray', write_file=None):
  """Plot image"""
  plt.figure(fig_num)
  plt.imshow(image, cmap=colormap)
  plt.title(name), plt.xticks([]), plt.yticks([])
  if write_file:
    cv2.imwrite(write_file, image)
  fig_num += 1
  return fig_num

def main():
  """Connected components"""
  # Configurations
  result_dir = './results'
  os.makedirs(result_dir,exist_ok=True)
  image_file = './images/tall_noise10_backgr.png'
  write_results = True

  # Step 1: Read image
  image = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE)
  fig_num = plot_image(image, 'Grayscale original', 0)
  image = image.astype(np.float32)
  if write_results:
    cv2.imwrite(os.path.join(result_dir, 'original.png'), image)

  # Here are some different blur functions you can try for both step 2 and
  # step 3.
  # ksize = 21 # Some odd integer
  # blurred_image = cv2.blur(image, (ksize, ksize)) # Mean blur
  # blurred_image = cv2.GaussianBlur(image, (ksize, ksize), 0)
  # blurred_image = cv2.medianBlur(image, ksize)
  # blurred_image = cv2.biliteralFilter(imag, 9, 75, 75) # Read the docs

  # Step 2: Remove high-frequency noise
  nr_image = cv2.GaussianBlur(image, (5, 5), 0)
  fig_num = plot_image(nr_image, 'Noise removed', fig_num)
  if write_results:
    cv2.imwrite(os.path.join(result_dir, 'noise_removed.png'), nr_image)

  # Step 3: Create background image
  background = cv2.GaussianBlur(nr_image, (21, 21), 0)
  fig_num = plot_image(background, 'Background', fig_num)
  if write_results:
    cv2.imwrite(os.path.join(result_dir, 'background.png'), background)

  # Step 4: Remove background
  br_image = nr_image - background
  # Scale the image to [0, 255] and cast it back to int
  br_image = 255*(br_image - np.min(br_image)) / (np.max(br_image) - np.min(br_image))
  br_image = br_image.astype(np.uint8)
  fig_num = plot_image(br_image, 'Background removed', fig_num)
  if write_results:
    cv2.imwrite(os.path.join(result_dir, 'background_removed.png'), br_image)

  # Step 5: Threshold the image using a global threshold
  fig = plt.figure(fig_num)
  plt.hist(br_image.flatten(), 256,  facecolor='black', alpha=0.75)
  plt.xlabel('Histogram of background removed image')
  fig.savefig('results/br_histogram.png', bbox_inches='tight',
              pad_inches=0)
  fig_num += 1
  threshold = 149
  thr_image = (br_image < threshold).astype(np.uint8)
  fig_num = plot_image(thr_image, 'Thresholded image at '+str(threshold), fig_num)
  if write_results:
    cv2.imwrite(os.path.join(result_dir, 'thresholded.png'), thr_image*255)

  # Step 7: Compute region objects and labels
  connectivity = 4
  output = cv2.connectedComponentsWithStats(thr_image,
                                            connectivity,
                                            cv2.CV_32S)
  #num_labels = output[0]
  label_image = output[1] # Image with a unique label for each connected region
  stats = output[2] # See below
  #centroids = output[3] # Centroid indices for each connected region



  fig_num = plot_image(label2rgb(label_image), 'Labels before thresholding', fig_num)
  if write_results:
    cv2.imwrite(os.path.join(result_dir, 'label_image.png'),
                label2rgb(label_image)*255) # from (0, 1) to (0, 255)

  # stats is a num_labels x 5 array containing the following information about
  # every connected component (component 0 is background).
  # stats[0]: The leftmost coordinate which is the inclusive start of the
  #           bounding box in the horizontal direction.
  # stats[1]: The topmost coordinate which is the inclusive start of the
  #           bounding box in the vertical direction.
  # stats[2]: The horizontal size of the bounding box.
  # stats[3]: The vertical size of the bounding box.
  # stats[4]: The total area (in pixels) of the connected component.

  # Step 8: Use information about region to remove noise and the frame

  # First, let us see if some areas are distinctive (we slice away
  # background, in our case we know that it is the one with the largest area)
  region_area = stats[1:, 4]
  fig = plt.figure(fig_num)
  plt.hist(region_area, 256,  facecolor='black', alpha=0.75)
  plt.xlabel('Region area')
  fig.savefig('results/area_histogram.png', bbox_inches='tight',
              pad_inches=0)
  fig_num += 1

  # Use the thresholds to exclude regions falling outside the interval
  lower_threshold = 200
  upper_threshold = 450
  keep_labels = np.where(np.logical_and(stats[:, 4] > lower_threshold,
                                        stats[:, 4] < upper_threshold))
  keep_label_image = np.in1d(label_image, keep_labels).reshape(label_image.shape)
  ra_thr_image = np.copy(thr_image)
  ra_thr_image[keep_label_image] = 255
  ra_thr_image[keep_label_image == False] = 0
  fig_num = plot_image(ra_thr_image, 'Thresholded image after area thresholding', fig_num)
  if write_results:
    filename = 'thresholded_region_area_{}_{}.png'.format(lower_threshold, upper_threshold)
    cv2.imwrite(os.path.join(result_dir, filename), ra_thr_image)

  # This seems to be sufficient, but let us also include bounding box area
  bbox_area = stats[1:, 2] * stats[1:, 3]
  plt.figure(fig_num)
  plt.scatter(region_area, bbox_area, s=5, facecolor='black')
  plt.xlabel('Region area')
  plt.ylabel('Bounding box area')
  fig.savefig('results/area_scatter.png', bbox_inches='tight',
              pad_inches=0)
  fig_num += 1

  plt.show()

if __name__ == "__main__":
  main()
