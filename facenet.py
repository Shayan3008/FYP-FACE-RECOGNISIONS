# function for face detection with mtcnn
from PIL import Image
import numpy  as np
from mtcnn.mtcnn import MTCNN
from keras.models import load_model
import matplotlib.pyplot as plt
import mmcv
import cv2
import math
def model_load():
    loaded_model = load_model('facenet_keras.h5')
    return loaded_model
def extract_face(filename): #for videos
    video = mmcv.VideoReader('video.mp4')
    frames = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in video]
    for i in range(len(frames)):
        frames[i].show()
        if i > 0:
            break
        image= frames[i]
        image = image.convert('RGB')
        pixels = np.asarray(image)
        detector = MTCNN()
        pixel = detector.detect_faces(pixels)
        # print(pixel)
        for i in range(len(pixel)):
            return (Extract_faces(pixels, pixel, i))
            break
            # face_array = asarray(image)
    return np.array([])
def embedding_extractor(fileName, model):#for single person image testing
    pixels = extract_face2(fileName)
    pixels = pixels.astype('float32')
    mean , std = pixels.mean() , pixels.std()
    pixels  = (pixels-mean) / std
    samples = np.expand_dims(pixels,axis = 0)
    embedding = model.predict(samples)
    return embedding[0]
def difference_image(image_array1,image_array2):
    difference  = abs(image_array1 - image_array2)
    print((difference.sum()/80)**2)
    return difference.sum()
def extract_face2(fileName): #for single person image 
    image = Image.open(fileName)
    image = image.convert('RGB')
    pixels = np.asarray(image)
    detector = MTCNN()
    pixel = detector.detect_faces(pixels)
        # print(pixel)
    for i in range(len(pixel)):
        return (Extract_faces(pixels, pixel, i))
            # face_array = asarray(image)
    return np.array([])
def Extract_faces(pixels, pixel, i):
    bgcolor = [255,255,255]
    x1,y1,width,height = pixel[i]['box']
    x1,y1 = abs(x1) , abs(y1)
    x2,y2 = x1+width,y1+height
    face = pixels[y1:y2,x1:x2]
    image = Image.fromarray(face)
    image = image.resize((160,160))
    image.save(str(i)+'.jpg')
    #image.show()
    return (np.asarray(image)/255)
    # image.show()
def embedding_extractors(faces,model):
    face_embeddings = []
    for i in range(len(faces)):
        pixels = faces[i].astype('float32')
        mean , std = pixels.mean() , pixels.std()
        pixels  = (pixels-mean) / std
        samples = np.expand_dims(pixels,axis = 0)
        embedding = model.predict(samples)
        face_embeddings.append(embedding[0])
    return face_embeddings
def extract_face_multiple(fileName):#for multiple person image
    faces = []
    image = Image.open(fileName)
    image = image.convert('RGB')
    pixels = np.asarray(image)
    # rgb = pixels[:,:,:3]
    # color = [246,213,139]
    # black = [0,0,0,255]
    # white = [255,255,255,255]
    # mask = np.all(rgb == color , axis = -1)
    # pixel = pixels.copy()

    # pixel[mask] = white
    # new_im = Image.fromarray(pixel)
    # new_im.show()
    detector = MTCNN()
    pixel = detector.detect_faces(pixels)
        # print(pixel)
    for i in range(len(pixel)):
        faces.append(Extract_faces(pixels, pixel, i))
    return faces
model = model_load()
face = extract_face_multiple('test_image8.jpg')
face.pop(len(face) - 1)
embedded_face = embedding_extractors(face,model)
target_embedding = embedding_extractor('test_image10.jpg', model)
min_distance = np.inf
selected_index = -1
for i in range(len(embedded_face)):
    dist = difference_image(target_embedding,embedded_face[i])
    if dist < min_distance:
        min_distance = dist
        selected_index = i
print(selected_index)
# print(difference_image(embedding_extractor('test_image9.jpg', model),embedding_extractor('test_image8.jpg',model)))