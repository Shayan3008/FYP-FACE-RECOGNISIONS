
import torch
import numpy as np
import mmcv
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from IPython import display
from facenet_pytorch import MTCNN,InceptionResnetV1

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


def extract_frames(device):
     video = mmcv.VideoReader('video.mp4')
     frames = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in video]

# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN(image_size=25600, margin=20)

# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2').eval()
img = Image.open('person.jpg')
    
# Get cropped and prewhitened image tensor
img_cropped = mtcnn(img)
if img_cropped == None:
    print('person.jpg')
# Calculate embedding (unsqueeze to add batch dimension)
img_embedding = InceptionResnetV1(img_cropped)
print(img_embedding)
# Or, if using for VGGFace2 classification
# resnet.classify = True
# img_probs = resnet(img_cropped)