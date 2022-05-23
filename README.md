# Mask_Recognition
University project to create a working mask recognition AI

# Task 1

Creating a UI, possibly a web browser UI to capture and take a photo of a face.
### Going to use Vite with vue.js for the UI

### Camera feed is available and can take a snapshot

# Running the website
To run the website clone the repository. Then make sure you are in root directory (mr) and open your preferred terminal. 
Make sure you have npm installed. In terminal run ```npm install vite``` and wait for it to install.
Make sure you have camera set as default camera device. When vite is installed run ```npm run dev``` and you will get localhost link.

# To start recognition from the website you will need to run python api
Python api is located mr/src/components/Face.py.
To run this code you will need to have installed cv2, flask, flask-restful, flask-cors, pillow.
To do so run ```pip install opencv-python flask flask-restful flask-cors pillow```.
## Updates where made to the api script therefore more dependencies are required!
# Before running the API in the terminal run ```pip install -r requirements.txt```
## If for some reason requirements.txt would fail to install or the API wouldn't launch then try solution bellow
* Try running `python train_mask_detector.py` which is in the src/components folder
* If above fails try `pip install tensorflow imutils matplotlib scipy sklearn`
* If all fails then try reading the console for errors and try to install libraries based on console output
When everything is installed you can run the api ```python Face.py```.

### Make sure both services are running for the website to send images to API

# You can now use `npm start` to open everything you need for the project to start
## Dependencies need to be installed!
# If there is no mode_detector.model file in src/components then first run `python train_mask_detector.py`