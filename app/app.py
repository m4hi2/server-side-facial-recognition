import base64
import io
import os
import random
import string
from io import StringIO
from threading import Event, Thread

import cv2
import face_recognition
import numpy as np
from flask import Flask, render_template
from flask.wrappers import Response
from flask_socketio import SocketIO, emit
from PIL import Image

from face_rec import FaceRec

thread = Thread()
stop_event = Event()

app = Flask(__name__)
app.config["DEBUG"] = True
socketio = SocketIO(app, logger=True)


@app.route('/')
def index():
    return render_template("index.html")


@socketio.on('user')
def new_user(user_id):
    print(user_id)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')
