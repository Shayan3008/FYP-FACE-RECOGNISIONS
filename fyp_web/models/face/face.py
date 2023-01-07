from keras.models import load_model
import cv2
from mtcnn.mtcnn import MTCNN
import numpy as np
from PIL import Image, ImageDraw


class Face:
    def __init__(self):
        self.model = load_model("models/face/facenet_keras.h5")
        self.faceDetect = MTCNN()

    def difference_image(self, image_array1, image_array2):
        difference = abs(image_array1 - image_array2)
        return (difference.sum()/80)**2

# Extract face embeddings

    def embedding_extractors(self, faces, model):
        face_embeddings = []
        for i in range(len(faces)):
            pixels = faces[i].astype('float32')
            mean, std = pixels.mean(), pixels.std()
            pixels = (pixels-mean) / std
            samples = np.expand_dims(pixels, axis=0)
            embedding = model.predict(samples)
            face_embeddings.append(embedding[0])
        return face_embeddings

    def extract_face_multiple(self, fileName, detector):  # for multiple person image
        faces = []
        image = Image.open(fileName)
        image = image.convert('RGB')
        pixels = np.asarray(image)
        pixel = detector.detect_faces(pixels)
        # print(pixel)
        for i in range(len(pixel)):
            faces.append(self.Extract_faces(pixels, pixel, i))
        return (faces, pixel)

    def extract_face2(self, image):  # for single person image
        image = image.convert('RGB')
        pixels = np.asarray(image)
        detector = MTCNN()
        pixel = detector.detect_faces(pixels)

        print(pixel)
        for i in range(len(pixel)):
            return (self.Extract_faces(pixels, pixel, i))
            # face_array = asarray(image)
        return np.array([])

    def embedding_extractor(self, image, model):  # for single person image testing
        pixels = self.extract_face2(image)
        print(pixels)
        pixels = pixels.astype('float32')
        mean, std = pixels.mean(), pixels.std()
        pixels = (pixels-mean) / std
        samples = np.expand_dims(pixels, axis=0)
        print(samples)
        embedding = model.predict(samples)
        if len(embedding) < 0:
            return 0
        else:
            return embedding[0]

    def Extract_faces(self, pixels, pixel, i):
        bgcolor = [255, 255, 255]
        x1, y1, width, height = pixel[i]['box']
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1+width, y1+height
        face = pixels[y1:y2, x1:x2]
        image = Image.fromarray(face)
        image = image.resize((160, 160))
        # image.save('test_'+str(i)+'.jpg')
        # image.show()
        return (np.asarray(image)/255)

    def extract_face_multiple(self, frame, detector):  # for multiple person image
        faces = []
        pixels = frame.copy()
        pixel = detector.detect_faces(pixels)
        # print(pixel)
        for i in range(len(pixel)):
            faces.append(self.Extract_faces(pixels, pixel, i))
        return (faces, pixel)

    def play_video(self, fileName, target_embedding):
        cap = cv2.VideoCapture(fileName)
        video = []

    # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Error opening video stream or file")
        i = 0
        # Read until video is completed
        while(cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            i = i+1
            if i % 25 != 0:
                if ret == True:
                    selected_index = -1
                    min_distance = np.inf
                    face = self.extract_face_multiple(
                        frame, detector=self.faceDetect)
                    embedded_face = self.embedding_extractors(
                        face[0], self.model)
                    print('EMBEDDING', len(embedded_face))
                    for i in range(len(embedded_face)):
                        dist = self.difference_image(
                            target_embedding, embedded_face[i])
                        print(dist)
                        if dist < min_distance and dist < 1.5:
                            min_distance = dist
                            selected_index = i
                    print('INDEX:', selected_index)
                    if selected_index != -1:
                        x1, y1, width, height = face[1][selected_index]['box']
                        x1, y1 = abs(x1), abs(y1)
                        x2, y2 = x1+width, y1+height
                        cv2.rectangle(frame, (x1, y1), (x2, y2),
                                      (0, 0, 255), 2)
                        # image.show()
                        array = np.array(image)
                        # cv_array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
                    image = cv2.resize(frame, (1280, 720))
                    video.append(image)
                    # break

                # Break the loop
                else:
                    break
        if len(video) > 0:
            height, width, layer = video[0].shape
            shapes = (width, height)
            out = cv2.VideoWriter(
                'static/project.mp4', cv2.VideoWriter_fourcc(*'H264'), 15, shapes)
            for i in range(len(video)):
                out.write(video[i])
            out.release()
        return '/static/project.mp4'
    # model = model_load()
    # detector = MTCNN
    # input_embedding = embedding_extractor('images/test_0.jpg', model)
    # # print(input_embedding)
    # play_video('', detector, input_embedding)
