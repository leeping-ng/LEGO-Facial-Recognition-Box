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

sys.path.insert(0, '..')
CONFIG_PATH = 'settings.yml'
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

while True:
    print("[INFO] Capturing image.")

    frame = vs.read()
    frame = cv2.flip(frame, 180)
    #frame = resize(frame, width=100)
    
    # SHOULD RESIZE TO SPEED UP, IT'S IN imutils.resize
    
    # Find all the faces and face encodings in the current frame of video
    # WIP: It may be faster to use haar cascades instead of this to detect faces
    face_locations = face_recognition.face_locations(frame)
    
    print("[INFO] Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    #for face_encoding in face_encodings:
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(whitelisted_face_encodings, face_encoding)
        name = "Unknown"
        
        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(whitelisted_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = whitelisted_face_names[best_match_index]
            open_box = True
            

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 255, 0), 1)

        print("I see someone named {}!".format(name))
    

    # display the image to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if open_box:
        # move motor and end program
        print("Opening box!")
        rotate_servo(settings['open_angle'])
        break

    

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

    fps.update()

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
