from PIL import Image, ImageDraw
import numpy as np
from mtcnn.mtcnn import MTCNN
from keras.models import load_model
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import mmcv
import cv2
import math


def model_load():
    loaded_model = load_model('facenet_keras.h5')
    return loaded_model


def difference_image(image_array1, image_array2):
    difference = abs(image_array1 - image_array2)
    print((difference.sum()/80)**2)
    return (difference.sum()/80)**2


def embedding_extractors(faces, model):
    face_embeddings = []
    for i in range(len(faces)):
        pixels = faces[i].astype('float32')
        mean, std = pixels.mean(), pixels.std()
        pixels = (pixels-mean) / std
        samples = np.expand_dims(pixels, axis=0)
        embedding = model.predict(samples)
        face_embeddings.append(embedding[0])
    return face_embeddings


def extract_face_multiple(fileName):  # for multiple person image
    faces = []
    image = Image.open(fileName)
    image = image.convert('RGB')
    pixels = np.asarray(image)
    detector = MTCNN()
    pixel = detector.detect_faces(pixels)
    # print(pixel)
    for i in range(len(pixel)):
        faces.append(Extract_faces(pixels, pixel, i))
    return (faces, pixel)


def extract_face2(fileName):  # for single person image
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


def embedding_extractor(fileName, model):  # for single person image testing
    pixels = extract_face2(fileName)
    pixels = pixels.astype('float32')
    mean, std = pixels.mean(), pixels.std()
    pixels = (pixels-mean) / std
    samples = np.expand_dims(pixels, axis=0)
    embedding = model.predict(samples)
    return embedding[0]


def Extract_faces(pixels, pixel, i):
    bgcolor = [255, 255, 255]
    x1, y1, width, height = pixel[i]['box']
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1+width, y1+height
    face = pixels[y1:y2, x1:x2]
    image = Image.fromarray(face)
    image = image.resize((160, 160))
    image.save(str(i)+'.jpg')
    # image.show()
    return (np.asarray(image)/255)
    # image.show()


model = model_load()
image = Image.open('test_image8.jpg')
image.convert('RGB')
data = plt.imread('test_image8.jpg')
# plt.imshow(data)
ax = plt.gca()
face = extract_face_multiple('test_image8.jpg')
embedded_face = embedding_extractors(face[0], model)
target_embedding = embedding_extractor('test_image12.jpg', model)
min_distance = np.inf
selected_index = -1
for i in range(len(embedded_face)):
    dist = difference_image(target_embedding, embedded_face[i])
    if dist < min_distance and dist < 1.3:
        min_distance = dist
        selected_index = i
print(selected_index)
img1 = ImageDraw.Draw(image)

if selected_index != -1:
    x1, y1, width, height = face[1][selected_index]['box']
    x1, y1 = abs(x1), abs(y1)
    x2,y2 = x1+width,y1+height
    img1.rectangle([(x1,y1),(x2,y2)], outline=(255, 0, 0), width=3)
    image.show()
    # x1, y1 = abs(x1), abs(y1)
    # rect = Rectangle((x1,y1-5),width+20,height+10,color ='orange' ,fill = False)
    # ax.add_patch(rect)
    # plt.show()
else:
    print('NO FACE MATCHED')