import cv2
import numpy as np

def draw_boxes(frame, bbox_list, color=(255,0,0)):
	"""Draws all the boxes in the list of boxes, and displays confidence
		bbox_list = [box1,box2,box3....etc]
		box1 = [x1, y1, x2, y2, Class, confidence]
		To draw the box, we need only the coordinates,
		box1[:4] = [x1, y1, x2, y2]
		box1[5] = confidence"""
	for box in bbox_list:
		x1, y1, x2, y2 = box[:4]	# We need the (x1, y1) and (x2, y2) coordinates only
		conf = box[5]
		cv2.rectangle(frame, pt1=(x1, y1), pt2=(x2, y2), color=color, thickness=2)
		frame = cv2.putText(frame, str(conf), (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX , 0.5, 
						(255, 255, 255), 1, cv2.LINE_AA) 	# Draw the IOU on the image
	return frame

def IOU(box1, box2):
	""" We assume that the box follows the format:
		box1 = [x1,y1,x2,y2], and box2 = [x3,y3,x4,y4],
		where (x1,y1) and (x3,y3) represent the top left coordinate,
		and (x2,y2) and (x4,y4) represent the bottom right coordinate """
	x1, y1, x2, y2 = box1
	x3, y3, x4, y4 = box2
	x_inter1 = max(x1, x3)
	y_inter1 = max(y1, y3)
	x_inter2 = min(x2, x4)
	y_inter2 = min(y2, y4)
	width_inter = abs(x_inter2 - x_inter1)
	height_inter = abs(y_inter2 - y_inter1)
	area_inter = width_inter * height_inter
	width_box1 = abs(x2 - x1)
	height_box1 = abs(y2 - y1)
	width_box2 = abs(x4 - x3)
	height_box2 = abs(y4 - y3)
	area_box1 = width_box1 * height_box1
	area_box2 = width_box2 * height_box2
	area_union = area_box1 + area_box2 - area_inter
	iou = area_inter / area_union
	return iou

def nms(boxes, conf_threshold=0.7, iou_threshold=0.4):
	"""
	The function performs nms on the list of boxes:
	boxes: [box1, box2, box3...]
	box1: [x1, y1, x2, y2, Class, Confidence]
	"""
	bbox_list_thresholded = []	# List to contain the boxes after filtering by confidence
	bbox_list_new = []			# List to contain final boxes after nms 
	# Stage 1: (Sort boxes, and filter out boxes with low confidence)
	boxes_sorted = sorted(boxes, reverse=True, key = lambda x : x[5])	# Sort boxes according to confidence
	for box in boxes_sorted:
		if box[5] > conf_threshold:		# Check if the box has a confidence greater than the threshold
			bbox_list_thresholded.append(box)	# Append the box to the list of thresholded boxes 
		else:
			pass
	#Stage 2: (Loop over all boxes, and remove boxes with high IOU)
	while len(bbox_list_thresholded) > 0:
		current_box = bbox_list_thresholded.pop(0)		# Remove the box with highest confidence
		bbox_list_new.append(current_box)				# Append it to the list of final boxes
		for box in bbox_list_thresholded:
			if current_box[4] == box[4]:				# Check if both boxes belong to the same class
				iou = IOU(current_box[:4], box[:4])		# Calculate the IOU of the two boxes
				if iou > iou_threshold:					# Check if the iou is greater than the threshold defined
					bbox_list_thresholded.remove(box)	# If there is significant overlap, then remove the box
	return bbox_list_new

def main():
	img = cv2.imread("Images/img.jpg")	# Read the image 
	img = cv2.resize(img, (416, 416))	# Resize the image to be displayed on the screen
	img_nms = img.copy()				# Create a copy of the image to draw on

	bbox_dog1 = [90, 261, 228, 378, "Dog", 0.9]		# Defining the different bounding boxes
	bbox_dog2 = [121, 290, 216, 374, "Dog", 0.6]	
	bbox_dog3 = [49, 265, 243, 388, "Dog", 0.85]	
	bbox_person1 = [234, 91, 359, 370, "Person", 0.95]	
	bbox_person2 = [239, 116, 359, 374, "Person", 0.45]	
	bbox_person3 = [234, 71, 359, 370, "Person", 0.92]	
	bbox_list = [bbox_dog1, bbox_dog2, bbox_dog3, bbox_person1, bbox_person2, bbox_person3]	# Creating the list of the boxes
	
	bbox_list_new = nms(bbox_list, conf_threshold=0.7, iou_threshold=0.4)	# Call the function to perform NMS

	img = draw_boxes(img, bbox_list)				# Draw all the boxes before nms
	img_nms = draw_boxes(img_nms, bbox_list_new)	# Draw all the boxes after nms
	img = cv2.putText(img, str("Before NMS"), (30, 30), cv2.FONT_HERSHEY_SIMPLEX , 1, 			# Write on the image before nms 
						(0, 0, 0), 2, cv2.LINE_AA) 		
	img_nms = cv2.putText(img_nms, str("After NMS"), (30, 30), cv2.FONT_HERSHEY_SIMPLEX , 1, 	# Write on the image after nms
						(0, 0, 0), 2, cv2.LINE_AA) 	
	cv2.imwrite("result.jpg", np.hstack((img, img_nms)))	# Write the image for reference 
	cv2.imshow("IMG", np.hstack((img, img_nms)))	# Stack the images horizontally and display
	cv2.waitKey()	# Wait for any key to be pressed to exit

if __name__ == "__main__":
	main()
