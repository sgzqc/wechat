import cv2

def draw_box(frame, bbox, color=(255,0,0)):
	x1, y1, x2, y2 = bbox
	cv2.rectangle(frame, pt1=(x1, y1), pt2=(x2, y2), color=color, thickness=2)
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

def main():
	bbox_cat1 = [130, 32, 450, 452]	# Defining the coordinates of the first bounding box (x1,y1,x2,y2)
	bbox_cat2 = [140, 42, 350, 447]	# Defining the coordinates of the second bounding box (x3,y3,x4,y4)
	img = cv2.imread("Images/Cat.jpg")	# Read the image 
	img = cv2.resize(img, (640, 480))	# Resize the image to be displayed on the screen
	img = draw_box(img,bbox_cat1,color=(0,255,0)) # Call the function to draw the first box	
	img = draw_box(img,bbox_cat2,color=(255,0,0)) # Call the function to draw the second box	
	iou = IOU(bbox_cat1, bbox_cat2)	# Calling the function to return the IOU
	img = cv2.putText(img, 'IOU: {}'.format(iou), (bbox_cat1[0], bbox_cat1[1]), cv2.FONT_HERSHEY_SIMPLEX , 1, 
						(255,0,0), 2, cv2.LINE_AA) 	# Draw the IOU on the image
	print("IOU OF THE BOXES IS: ", iou)	# Print the iou
	cv2.imshow("IMG", img)	# Show the image
	cv2.waitKey(0)	# Wait for any key to be pressed to exit

if __name__ == "__main__":
	main()
