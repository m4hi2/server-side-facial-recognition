import json

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["DEBUG"] = True
socketio = SocketIO(app, logger=True)

# temporary holding the notice
category = {
    "1604006": "Student",
    "Md. Rakib": "Teacher",
    "Unknown": "Unknown",
}

notices = {
    "Student": {
        'notice': ['Online Class'],
        'pages': 1
    },
    "Teacher": {
        'notice': ['Seminar Schedule', 'Online Class'],
        'pages': 5
    },
    "Unknown": {
        'notice': ['Admission Test Reschedule'],
        'pages': 1
    }
}

dept = {
    "1604006": "ETE",
    "Md. Rakib": "ETE",
    "Unknown": "Unknown"
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
    data = {
        "current_user": user_id,
        "category": cat,
        "notices": notices[cat],
        "dept": dept[user_id]

    }
    emit("user_info", json.dumps(data), broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1')
