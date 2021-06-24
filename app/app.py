from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["DEBUG"] = True
socketio = SocketIO(app, logger=True)

# temporary holding the notice
category = {
    "1604006": "Student",
    "Md. Rakib": "Teacher",
}

notices = {
    "Student": [],
    "Teacher": []

}


@app.route('/')
def index():
    return render_template("index.html")


@socketio.on('user')
def new_user(user_id):
    print(user_id)
    cat = category[user_id]
    print(category[user_id])
    print(notices[cat])


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')
