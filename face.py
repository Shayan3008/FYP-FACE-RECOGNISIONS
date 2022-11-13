
import torch
import numpy as np
import mmcv
import cv2

from PIL import Image, ImageDraw
from IPython import display
import sys
from mtcnn.mtcnn import MTCNN
import matplotlib.pyplot as plt
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


def display_video():
    try:
        # Create a VideoCapture object and read from input file
        cap = cv2.VideoCapture('video.mp4')
        
        # Check if camera opened successfully
        if (cap.isOpened()== False):
            print("Error opening video file")
        
        # Read until video is completed
        while(cap.isOpened()):
            
        # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == True:
            # Display the resulting frame
                cv2.imshow('Frame', frame)
                
            # Press Q on keyboard to exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        
        # Break the loop
            else:
                break
        
        # When everything done, release
        # the video capture object
        cap.release()
        
        # Closes all the frames
        cv2.destroyAllWindows()
    except:
        print('video.mp4')

def display_video2(frames):
    try:
    
        pil_image =Image.open(frames[0]).convert('RGB') 
        open_cv_image = np.array(pil_image) 
        # Convert RGB to BGR 
        open_cv_image = open_cv_image[:, :, ::-1].copy() 
        
        cv2.imshow('Frame', open_cv_image)
                    
        cv2.destroyAllWindows()
    except Exception as e:
        print(e)

def getFrames(device):
    video = mmcv.VideoReader('video.mp4')
    frames = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in video]
    mtcnn = MTCNN(device=device)
    frames_tracked = []
    for i, frame in enumerate(frames):
        print('\rTracking frame: {}'.format(i + 1), end='')
        
        # Detect faces
        boxes  = mtcnn.detect(frame)
        
        # Draw faces
        frame_draw = frame.copy()
        draw = ImageDraw.Draw(frame_draw)
        for box in boxes[0]:
            draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
        
        # Add to frame list
        frames_tracked.append(frame_draw.resize((640, 360), Image.BILINEAR))
    print('\nDone')
    return frames_tracked


def extract_image_from_detector(device):
    count = 0
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture('video.mp4')
    frames_tracked = []
    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video file")
        
    # Read until video is completed
    while cap.isOpened():
        ret,frames = cap.read()
        if ret:
            print(type(frames))
            mtcnn = MTCNN(device = device)
            for i, frame in enumerate(frames):
                print('\rTracking frame: {}'.format(i + 1), end='')
                
                # Detect faces
                boxes  = mtcnn.detect(frame)
                frame_data = frame.copy()
                for box in boxes[0]:
                    x1,y1,width,height = box
                    x2,y2 = x1+width,y1+height
                    image = frame_data[x1:x2,y1:y2]
                    plt.imshow(image)
                    break
                break

        else:
            break
    
    return frames_tracked

# im = getFrames(device)[0]
# im.save('output.jpg')

extract_image_from_detector(device=device)