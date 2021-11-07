from flask import Flask, render_template, request
from flask_socketio import SocketIO

# Flask documentation:
# https://flask.palletsprojects.com/en/2.0.x/quickstart/#static-files
app = Flask(__name__)

# documentation to get Flask to support SocketIO:
# https://flask-socketio.readthedocs.io/en/latest/getting_started.html
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/")
def question_page():
    return render_template("question.html")


@app.route("/scoreboard")
def scoreboard():
    return render_template("scoreboard.html")


@app.route("/login")
def login():
    return "tbd"


@socketio.on('answer')
def button_pressed(jsondata):
    # send to database
    return "tbd"


if __name__ == '__main__':
    socketio.run(app)
