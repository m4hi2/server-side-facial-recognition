import base64
import os

import cv2
import eventlet
import face_recognition
import numpy as np
import socketio
from eventlet.green.threading import Event, Thread

camera = cv2.VideoCapture(0)

sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

thread = Thread()
thread_stop_event = Event()
mahir_image = face_recognition.load_image_file(
    os.path.realpath("/home/m4hi2/Pictures/Webcam/m2.jpg"))
mahir_face_encoding = face_recognition.face_encodings(mahir_image)[0]
rakib_image = face_recognition.load_image_file(
    os.path.realpath("/home/m4hi2/Pictures/Webcam/rakib.jpg")
)
rakib_face_encoding = face_recognition.face_encodings(rakib_image)[0]


known_face_encodings = [
    mahir_face_encoding,
    rakib_face_encoding
]

known_face_names = [
    "1604006",
    "Md. Rakib"
]
face_locations = []
face_encodings = []
face_names = []

CURRENT_USER = ""


def capture_and_send():
    while not thread_stop_event.isSet():
        global CURRENT_USER
        _, frame = camera.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_frame, face_locations)
        face_names = []
        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)

            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
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
            top = top - 30
            bottom = bottom + 30
            right = right + 20
            left = left - 20
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

            if CURRENT_USER not in face_names and name != "Unknown":
                CURRENT_USER = name
                sio.emit("user", CURRENT_USER, broadcast=True)

        _, imgencode = cv2.imencode(".jpg", frame)
        stringData = base64.b64encode(imgencode).decode('utf-8')
        b64_src = 'data:image/jpeg;base64,'
        stringData = b64_src + stringData

        sio.emit("response_back", stringData, broadcast=True)
        sio.sleep(.1)
        face_names = []


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    global thread

    if not thread.is_alive():
        thread = sio.start_background_task(capture_and_send)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5050)), app)
