import base64
import os

import cv2
import eventlet
import face_recognition
import numpy as np
import socketio
from eventlet.green.threading import Event, Thread

camera = cv2.VideoCapture(0)

sio = socketio.Server(logger=True)
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

thread = Thread()
thread_stop_event = Event()
mahir_image = face_recognition.load_image_file(
    os.path.realpath("/home/m4hi2/Pictures/Webcam/m2.jpg"))
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


def capture_and_send():
    while not thread_stop_event.isSet():
        _, frame = camera.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # small_frame = frame

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

        _, imgencode = cv2.imencode(".jpg", frame)
        stringData = base64.b64encode(imgencode).decode('utf-8')
        b64_src = 'data:image/jpeg;base64,'
        stringData = b64_src + stringData
        sio.emit("response_back", stringData, broadcast=True)
        sio.sleep(.1)


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    global thread

    if not thread.is_alive():
        thread = sio.start_background_task(capture_and_send)


if __name__ != '__main__':
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app)
