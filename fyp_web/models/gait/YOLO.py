import numpy as np
import cv2
import os
import imutils
from PIL import Image




def pedestrian_detection(image, model, layer_name, personidz,MIN_CONFIDENCE,NMS_THRESHOLD):
	(H, W) = image.shape[:2]
	results = []
	# print(personidz)
	# print(MIN_CONFIDENCE)
	# print(NMS_THRESHOLD)

    
	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	# print(layer_name)
	# print("This is BLOBS",blob)
	
	model.setInput(blob)
	print(layer_name)
	layerOutputs = model.forward(layer_name)
	print("This is layer outputs",layerOutputs)
	boxes = []
	centroids = []
	confidences = []

	for output in layerOutputs:
		for detection in output:

			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			if classID == personidz and confidence > MIN_CONFIDENCE:

				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				boxes.append([x, y, int(width), int(height)])
				centroids.append((centerX, centerY))
				confidences.append(float(confidence))
	# print(boxes)
	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idzs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONFIDENCE, NMS_THRESHOLD)
	# print("This is the id of YOLO MODEL:",len(idzs))
	# ensure at least one detection exists
	if len(idzs) > 0:
		# loop over the indexes we are keeping
		for i in idzs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
			# update our results list to consist of the person
			# prediction probability, bounding box coordinates,
			# and the centroid
			res = (confidences[i], (x, y, x + w, y + h), centroids[i])
			results.append(res)
            
	# return the list of results
	return results




def play():
    NMS_THRESHOLD=0.3
    MIN_CONFIDENCE=0.2
    labelsPath = "./models/gait/coco.names"
    LABELS = open(labelsPath).read().strip().split("\n")
    print(LABELS)
    weights_path = "./models/gait/yolov4_tiny.weights"
    config_path = "./models/gait/yolov4_tiny.cfg"
    

    model = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    print(model.empty())
    layer_name = model.getLayerNames()
    layer_name = [layer_name[i - 1] for i in model.getUnconnectedOutLayers()]
    cap = cv2.VideoCapture("./static/CameraVideos/test8.mp4")
    writer = None
    while cap.isOpened():
	
        (grabbed, image) = cap.read()
        if not grabbed:
            break
            
        image = imutils.resize(image, width=700)
        results = pedestrian_detection(image, model, layer_name,
            LABELS.index("person"),MIN_CONFIDENCE,NMS_THRESHOLD)
        print("THIS IS THE RESULTS:\n",results)
        
        x = results[0][1][0]
        y = results[0][1][1]
        w = results[0][1][2]
        h = results[0][1][3]
            
        roi_extract = image[y:h,x:w]
        print(len(roi_extract))
        if len(roi_extract) > 0:
            roi_arr = Image.fromarray(roi_extract).show()
            

    cap.release()
    cv2.destroyAllWindows()