import numpy as np
import cv2  # Import the OpenCV library to enable computer vision
import numpy as np  # Import the NumPy scientific computing library
from imutils.object_detection import non_max_suppression  # Handle overlapping
from PIL import Image
from models.gait.reid import REID
from models.face.face import Face

import os
import imutils



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

def calculate_distance(source, target):
    # print(target.sum())
    difference = abs(source-target)
    # print(difference.sum())
    print(difference.sum()/200)
    return (difference.sum())/200


def load_model():
    return REID()


def extract_features(reid, input):
    data = reid._features(input)
    return data



def main(reid, inputImageFileName, inputVideoFileName):
    i = 0
    NMS_THRESHOLD=0.3
    MIN_CONFIDENCE=0.2
    labelsPath = "./models/gait/coco.names"
    LABELS = open(labelsPath).read().strip().split("\n")
    weights_path = "./models/gait/yolov4_tiny.weights"
    config_path = "./models/gait/yolov4_tiny.cfg"
    

    model = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    layer_name = model.getLayerNames()
    layer_name = [layer_name[i - 1] for i in model.getUnconnectedOutLayers()]
    # cap = cv2.VideoCapture("./static/CameraVideos/test8.mp4")
    # writer = None

    min_dist_gait = 1000
    # faceModel = Face()
    cap = cv2.VideoCapture(inputVideoFileName)
    file_size = (1920, 1080)
    scale_ratio = 1
    output_filename = 'output9.mp4'
    output_frames_per_second = 20.0
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    result = cv2.VideoWriter("./static/output9.mp4", fourcc, 30.0, (1280, 720))
    input_image = Image.open(inputImageFileName)
    # faceInputEmbedding = faceModel.embedding_extractor(input_image, faceModel.model)

    image = []
    image.append(np.array(input_image))
    # print(extract_features(image)[0])
    temp = extract_features(reid, image)[0]
    src = temp.data.cpu().numpy()


    # Process the video
    while cap.isOpened():
        
        # Capture one frame at a time
        success, frame = cap.read()

        # Do we have a video frame? If true, proceed.
        if success:
            if i == 2:
                i = 0
            else:
            # Resize the frame
                width = int(frame.shape[1] * scale_ratio)
                height = int(frame.shape[0] * scale_ratio)
                frame = cv2.resize(frame, (width, height))

                # Store the original frame
                orig_frame = frame.copy()
                # image = imutils.resize(frame, width=700)
                results = pedestrian_detection(frame, model, layer_name,
                LABELS.index("person"),MIN_CONFIDENCE,NMS_THRESHOLD)
                temp2 = []
                bounding_box = []
                for res in results:
                    x = res[1][0]
                    y = res[1][1]
                    w = res[1][2]
                    h = res[1][3]
                    image_width = orig_frame.shape[1]
                    image_height = orig_frame.shape[0]
                    if w > image_width:
                         w = w - x
                    if h > image_height:
                         h = h - y
                    ROI = orig_frame[y:h,x:w]
                    temp2.append(ROI)
                    bounding_box.append(res[1])
                if len(temp2) > 0:
                    print("THIS IS DIMENSIONS:"+str(x)+" "+str(y)+" "+str(w)+" "+str(h))
                    dest = extract_features(reid, temp2)
                    selected_index = -1
                    min_distance = 10000
                    min1 = 1000
                    for i in range(len(dest)):
                        
                        if True:
                            
                            dist = calculate_distance(
                                src, dest[i].data.cpu().numpy())
                            if dist < min1 :
                                selected_index = i
                                min1 = dist
                        
                        else:
                            difference = faceModel.difference_image(
                                faceInputEmbedding, face_embedding)
                            if difference < min_dist_face and difference < threshold_face:
                                threshold_face = difference
                                selected_index = i
                                min_dist_face = dist

                    print('Selected Index: ', selected_index)
                    
                    cv2.rectangle(frame,
                                (bounding_box[selected_index][0],
                                bounding_box[selected_index][1]),
                                (bounding_box[selected_index][2],
                                    bounding_box[selected_index][3]),
                                (0, 0, 255),
                                2)
                
                image.append(frame)
              
                # result.write(image)
                i = i + 1
        else:
            break
        
    for i in range(len(image)):
        result.write(frame)
         
    # Stop when the video is finished
    cap.release()

    # Release the video recording
    result.release()

    # Close all windows
    # cv2.destroyAllWindows()

    return '/static/'+output_filename


# main('/static/project.mp4','/static/project.mp4')
