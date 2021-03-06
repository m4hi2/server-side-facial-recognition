import base64
import io
from io import StringIO

import cv2
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
    frame = cv2.flip(frame, 1)

    _, imgencode = cv2.imencode(".jpg", frame)

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpeg;base64,'
    stringData = b64_src + stringData
    emit('response_back', stringData)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')
