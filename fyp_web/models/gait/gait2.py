import numpy as np
import cv2  # Import the OpenCV library to enable computer vision
import numpy as np  # Import the NumPy scientific computing library
from imutils.object_detection import non_max_suppression  # Handle overlapping
from PIL import Image
from models.gait.reid import REID
from models.face.face import Face
import os
import imutils
min_dist_gait = 10000
threshold_gait = 10000
NMS_THRESHOLD=0.3
MIN_CONFIDENCE=0.2
min_dist_face = 10000
threshold_face = 10000
labelsPath = "./models/gait/coco.names"
LABELS = open(labelsPath).read().strip().split("\n")
weights_path = "./models/gait/yolov4-tiny.weights"
config_path = "./models/gait/yolov4-tiny.cfg"
model = cv2.dnn.readNetFromDarknet(config_path, weights_path)
layer_name = model.getLayerNames()
layer_name = [layer_name[i - 1] for i in model.getUnconnectedOutLayers()]
writer = None

def pedestrian_detection(image, model, layer_name, personidz=0):
	(H, W) = image.shape[:2]
	results = []


	blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	model.setInput(blob)
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
	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idzs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONFIDENCE, NMS_THRESHOLD)
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
    return (pow((difference.sum())/600, 1))


def load_model():
    return REID()


def extract_features(reid, input):
    data = reid._features(input)
    return data


def main(reid, inputImageFileName, inputVideoFileName):
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

            # Resize the frame
            width = int(frame.shape[1] * scale_ratio)
            height = int(frame.shape[0] * scale_ratio)
            frame = cv2.resize(frame, (width, height))

            # Store the original frame
            orig_frame = frame.copy()
            image = imutils.resize(frame, width=700)
            results = pedestrian_detection(frame, model, layer_name,
            personidz=LABELS.index("person"))
            temp2 = []
            bounding_box = []
            for res in results:
                x = res[1][0]
                y = res[1][1]
                w = res[1][2]
                h = res[1][3]
                ROI = orig_frame[y:h,x:w]
                image = Image.fromarray(ROI)
                image.show()
                temp2.append(np.array(ROI))
                bounding_box.append(res[1])
            # Draw bounding boxes on the framepixels
            # for (x, y, w, h) in bounding_boxes:

            #     x, y = abs(x), abs(y)
            #     x2, y2 = x+w, y+h
            #     image = Image.fromarray(frame)
            #     image.crop((x,y,x2,y2))
            #     print('HELLO WORLD')
            #     image = image.resize((160, 160))
            #     image.save('image1.jpg')
            #     temp2.append(np.array(image))
            #     bounding_box.append((x, y, w, h))
            # print(len(temp2))
            if len(temp2) > 0:

                # print(temp2)
                dest = extract_features(reid, temp2)
                # print('dest: ', len(dest))
                selected_index = -1
                min_distance = 10000
                for i in range(len(dest)):
                    # face_embedding = faceModel.embedding_extractor(
                    #     temp2[i], faceModel.model)
                    if True:
                        dist = calculate_distance(
                            src, dest[i].data.cpu().numpy())
                        # print(dist)
                        if dist < min_dist_gait and dist < threshold_gait:
                            threshold_gait = dist
                            selected_index = i
                            min_dist_gait = dist
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
            # image = cv2.resize(frame, (1280, 720))

            result.write(image)
        else:
            break

    # Stop when the video is finished
    cap.release()

    # Release the video recording
    result.release()

    # Close all windows
    cv2.destroyAllWindows()

    return '/static/'+output_filename


# main('/static/project.mp4','/static/project.mp4')
