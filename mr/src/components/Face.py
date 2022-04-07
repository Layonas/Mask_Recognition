from ast import arg
from distutils.log import debug
import cv2
import sys
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from io import BytesIO
import base64
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("blob")

class Predict(Resource):
    def post(self):
        args = parser.parse_args()

        code = base64.b64decode(args["blob"].split(',')[1]) 
        npimg = np.fromstring(code, np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        cascPath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)

        # Read the image
        #image = cv2.imread(image_decoded)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

        _, im_arr = cv2.imencode('.jpg', image)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)

        return im_b64.decode("utf-8")

        

api.add_resource(Predict, "/predict")
if __name__ == "__main__":
  app.run(debug=True)

# neliesk situ


