import threading
from time import sleep

import cv2
import face_recognition
import numpy as np


class FaceRec(object):
    def __init__(self, known_face_encodings, known_face_names):
        self.known_face_encodings = known_face_encodings
        self.known_face_names = known_face_names
        self.to_process = []
        self.to_output = []

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def process(self):
        if not self.to_process:
            return

        incoming_frame = self.to_process.pop(0)

        # TODO: Image processing on the frame

        output_frame = incoming_frame

        self.to_output.append(output_frame)

    def keep_processing(self):
        while True:
            self.process()
            sleep(0.01)

    def enqueue_input(self, in_frame):
        self.to_process.append(in_frame)

    def get_frame(self):
        while not self.to_output:
            sleep(0.05)
        return self.to_output.pop(0)
