from ast import arg
from distutils.log import debug
from re import T
import cv2
import sys
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from io import BytesIO
import base64
import numpy as np
from PIL import Image

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import imutils
import time
import os

import subprocess

exec(open(r"src\components\train_mask_detector.py").read())


app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("blob")

# load our serialized face detector model from disk
prototxtPath = r"src\components\face_detector\deploy.prototxt"
weightsPath = r"src\components\face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

class Preload():
    def load():
        return "Veikia"

preload = Preload

def detect_and_predict_mask(frame, faceNet, maskNet):
    # grab the dimensions of the frame and then construct a blob
	# from it
    (h, w) = frame.shape[:2]    
    # framer = cv2.resize(frame, (224, 224))
    blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
        (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()
    print(detections.shape)

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > 0.5:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)


class Predict(Resource):
    def post(self):
        # args = parser.parse_args()

        # code = base64.b64decode(args["blob"].split(',')[1]) 
        # npimg = np.fromstring(code, np.uint8)
        # image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # cascPath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        # faceCascade = cv2.CascadeClassifier(cascPath)

        # # Read the image
        # #image = cv2.imread(image_decoded)
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # # Detect faces in the image
        # faces = faceCascade.detectMultiScale(
        #     gray,
        #     scaleFactor=1.1,
        #     minNeighbors=5,
        #     minSize=(30, 30),
        #     flags = cv2.CASCADE_SCALE_IMAGE
        # )
        
        # # Draw a rectangle around the faces
        # for (x, y, w, h) in faces:
        #     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # _, im_arr = cv2.imencode('.jpg', image)  # im_arr: image in Numpy one-dim array format.
        # im_bytes = im_arr.tobytes()
        # im_b64 = base64.b64encode(im_bytes)

        # return preload.load()
        # #return im_b64.decode("utf-8")


        args = parser.parse_args()

        code = base64.b64decode(args["blob"].split(',')[1]) 
        npimg = np.fromstring(code, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        frame = imutils.resize(frame, width=854)

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            cv2.putText(frame, label, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        
        # frame = cv2.resize(frame, (480, 360))
        _, im_arr = cv2.imencode('.jpg', frame)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)

        # return preload.load()
        return im_b64.decode("utf-8")


# load the face mask detector model from disk
maskNet = load_model(r"src\components\mask_detector_224x224.model")

api.add_resource(Predict, "/predict")
if __name__ == "__main__":
  app.run(debug=True)

# neliesk situ


