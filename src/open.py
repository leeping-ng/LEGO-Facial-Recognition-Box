"""
Source code adapted from:
Title: Examples using face_recognition library
Author: Adam Geitgey
Date: 19 Jan 2020
Availability: https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam.py
"""

print("[INFO] Importing required libraries...")
import sys
import time
import numpy as np
import cv2

import face_recognition
from picamera import PiCamera

from utils.videostream import VideoStream
from utils.fps import FPS
from utils.servomotor import init_servo, rotate_servo
from utils.preprocessing import resize
from utils.read_config import extract_config
from utils.face_embeddings import create_embeddings
print("[INFO] Libraries imported!")

CONFIG_PATH = 'settings.yml'
HAAR_CASCADES_PATH = 'detector_architectures/haarcascade_frontalface_default.xml'

# read in configuration settings
sys.path.insert(0, '..')
settings = extract_config(CONFIG_PATH)

# create face embeddings from face images in folder
whitelisted_face_names, whitelisted_face_encodings = create_embeddings(settings)

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(resolution=(320, 240), framerate=32).start()
time.sleep(2.0)
fps = FPS().start()

# Initialize some variables
face_locations = []
face_encodings = []
init_servo()
open_box = False

# Loop through video frames
while True:
    # stop the program if there are no whitelisted faces, as there's no point in running
    if not whitelisted_face_names:
        print("[WARNING] No one has been granted access. Check that:")
        print("[WARNING] 1) Face images have been placed in the designated folder")
        print("[WARNING] 2) Whitelisted names have been set in settings.yml")
        print("[WARNING] 3) The filenames of the images and whitelisted names match")
        break

    print("[INFO] Capturing video frame.")
    frame = vs.read()
    frame = cv2.flip(frame, 180)
    # resize to increase frame rate, if needed
    #frame = resize(frame, width=100)   
    
    # Step 1: Detect the faces in the frame
    if settings['use_accurate_detector']:
        # Use HOG (more accurate, but slower)
        face_locations = face_recognition.face_locations(frame)
    else:
        # Use Haar Cascades (faster, but less accurate)
        haar_detector = cv2.CascadeClassifier(HAAR_CASCADES_PATH)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # recommended parameters: https://stackoverflow.com/questions/20801015/recommended-values-for-opencv-detectmultiscale-parameters
        vertices = haar_detector.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        face_locations = [(y, x + w, y + h, x) for (x, y, w, h) in vertices]
    print("[INFO] Found {} faces in image.".format(len(face_locations)))

    # Step 2: Use pre-trained NN to create 128-dim embeddings from detected faces
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop over each face found in the frame to see if it's whitelisted
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Step 3: See if the face is a match for the whitelisted face(s), a list of booleans
        matches = face_recognition.compare_faces(whitelisted_face_encodings, face_encoding)
        name = "Unknown"
        
        # Use the whitelisted face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(whitelisted_face_encodings, face_encoding)

        best_match_index = np.argmin(face_distances)
        # If true, grant access and open box
        if matches[best_match_index]:
            name = whitelisted_face_names[best_match_index]
            open_box = True
          
        # Draw a box around the face with associated name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left+6, top-6), font, 0.5, (0, 255, 0), 1)
        print("[INFO] {} detected.".format(name))

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if open_box:
        # move motor and end program
        print("Access has been granted to: {}".format(name))
        rotate_servo(settings['open_angle'])
        break

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# cleanup
cv2.destroyAllWindows()
vs.stop()

