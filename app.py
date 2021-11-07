from flask import Flask, render_template, request, url_for
from flask_socketio import SocketIO, emit, send

import main
import json

# Flask documentation:
# https://flask.palletsprojects.com/en/2.0.x/quickstart/#static-files
app = Flask(__name__)

# documentation to get Flask to support SocketIO:
# https://flask-socketio.readthedocs.io/en/latest/getting_started.html
# app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)


@app.route("/")
def question_page():
    return render_template("question.html")


@app.route("/scoreboard")
def scoreboard():
    return render_template("scoreboard.html")


@socketio.on('answer')
def button_pressed(jsondata):
    # Handle the choice for the user
    data = json.loads(jsondata)
    main.increment("connection thingy", data[data], -1)
    print(jsondata)

    # Emit something for the user to say if they follow the hive or not!
    # emit('answer_callback', json.dumps({"You are with the hive!"}))
    emit("answer", {"message" : "you are with the hive"}, json=True)

    print("message should have sent!")
    pass


if __name__ == '__main__':
    socketio.run(app)
