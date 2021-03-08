import base64
import io
import os
from io import StringIO

import cv2
import face_recognition
import numpy as np
from flask import Flask, render_template
from flask.wrappers import Response
from flask_socketio import SocketIO, emit
from PIL import Image

from face_rec import FaceRec

app = Flask(__name__)
app.config["DEBUG"] = True
socketio = SocketIO(app)

curr_path = os.path.dirname(__file__)

mahir_image = face_recognition.load_image_file(
    os.path.realpath("known_images/mahir.jpg"))
mahir_face_encoding = face_recognition.face_encodings(mahir_image)[0]


known_face_encodings = [
    mahir_face_encoding,
]

known_face_names = [
    "Mahir"
]
face_locations = []
face_encodings = []
face_names = []

face_rec = FaceRec(known_face_encodings=known_face_encodings,
                   known_face_names=known_face_names)


def facerec(frame):
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if True:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    # process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 1.0, (255, 255, 255), 1)
    return frame


@app.route('/')
def index():
    return render_template("index.html")


@socketio.on('image')
def image(data_image):
    subf = StringIO()
    subf.write(data_image)

    # decode image and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    # converting RGB to BGR, as openCV standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # process the image frames
    # frame = facerec(frame)
    face_rec.enqueue_input(frame)
    frame = face_rec.get_frame()

    _, imgencode = cv2.imencode(".jpg", frame)

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpeg;base64,'
    stringData = b64_src + stringData
    emit('response_back', stringData)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')
