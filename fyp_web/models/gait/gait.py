import numpy as np
import cv2  # Import the OpenCV library to enable computer vision
import numpy as np  # Import the NumPy scientific computing library
from imutils.object_detection import non_max_suppression  # Handle overlapping
from PIL import Image
from models.gait.reid import REID
from models.face.face import Face
# print(os.getcwd())
min_dist = 10000
# from PIL import Image

# from ipynb.fs.full.main import extract_features


def calculate_distance(source, target):
    print(target.sum())
    difference = abs(source-target)
    # print(difference.sum())
    return (pow((difference.sum())/600, 1))


def load_model():
    return REID()


def extract_features(reid, input):
    data = reid._features(input)
    return data


def main(reid, inputImageFileName, inputVideoFileName):
    # face = Face()
    file_size = (1920, 1080)
    scale_ratio = 1
    output_filename = 'output9.mp4'
    output_frames_per_second = 20.0
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    result = cv2.VideoWriter("./static/FinalGait.mp4", fourcc, 20.0, (1280, 720))

    image = []
    image.append(np.array(Image.open(inputImageFileName)))
    # print(extract_features(image)[0])
    temp = extract_features(reid, image)[0]
    src = temp.data.cpu().numpy()

# Create a HOGDescriptor object
    hog = cv2.HOGDescriptor()

    # Initialize the People Detector
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Load a video
    cap = cv2.VideoCapture(inputVideoFileName)

    # Create a VideoWriter object so we can save the video output
    # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # result = cv2.VideoWriter(output_filename,
    #                          fourcc,
    #                          output_frames_per_second,
    #                          file_size)

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

            (bounding_boxes, weights) = hog.detectMultiScale(frame,
                                                             winStride=(
                                                                 16, 16),
                                                             padding=(4, 4),
                                                             scale=1.05)
            temp2 = []
            bounding_box = []
            # Draw bounding boxes on the framepixels
            for (x, y, w, h) in bounding_boxes:

                x, y = abs(x), abs(y)
                x2, y2 = x+w, y+h
                face = orig_frame[y:y2, x:x2]
                image = Image.fromarray(face)
                image = image.resize((160, 160))
                image.save('INPUT.jpg')
                temp2.append(np.array(image))
                bounding_box.append((x, y, w, h))
            if len(temp2) > 0:

                # print(temp2)
                dest = extract_features(reid, temp2)
                # print('dest: ', len(dest))
                selected_index = -1
                min_distance = 10000
                for i in range(len(dest)):
                    dist = calculate_distance(src, dest[i].data.cpu().numpy())
                    # print(dist)
                    if dist < min_distance and dist < 1.9:
                        selected_index = i
                        min_distance = dist
                print('Selected Index: ', selected_index)

                cv2.rectangle(frame,
                              (bounding_box[selected_index][0],
                               bounding_box[selected_index][1]),
                              (bounding_box[selected_index][0] + bounding_box[selected_index][2],
                                  bounding_box[selected_index][1] + bounding_box[selected_index][3]),
                              (0, 0, 255),
                              2)
            image = cv2.resize(frame, (1280, 720))

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
