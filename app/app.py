from flask import Flask, render_template
from flask_socketio import SocketIO, emit

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
