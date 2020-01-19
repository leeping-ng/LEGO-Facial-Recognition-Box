
print("Importing required libraries...")
import time
import numpy as np
import cv2
from picamera import PiCamera
import face_recognition
from videostream import VideoStream
print("Libraries imported!")

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
subject_image = face_recognition.load_image_file("leeping.jpg")
subject_face_encoding = face_recognition.face_encodings(subject_image)[0]
print("Face embedding created!")

# Initialize some variables
face_locations = []
face_encodings = []


# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0, usePiCamera=True).start()
time.sleep(2.0)

while True:
    print("Capturing image.")

    frame = vs.read()
    # SHOULD RESIZE TO SPEED UP, IT'S IN imutils.resize
    
    # Find all the faces and face encodings in the current frame of video
    # WIP: It may be faster to use haar cascades instead of this to detect faces
    face_locations = face_recognition.face_locations(frame)
    
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop over each face found in the frame to see if it's someone we know.
    #for face_encoding in face_encodings:
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([subject_face_encoding], face_encoding)
        name = "<Unknown Person>"

        if match[0]:
            name = "Lee Ping"

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 255, 0), 1)

        print("I see someone named {}!".format(name))

    # display the image to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            break


# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

