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

app = Flask(__name__)
app.config["DEBUG"] = True
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template("index.html")


@socketio.on('user')
def new_user(user_id):
    print(user_id)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')
