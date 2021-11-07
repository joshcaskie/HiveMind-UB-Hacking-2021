from flask import Flask, render_template, request, make_response, url_for
from flask_socketio import SocketIO, emit, send

import main
import json

# https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python
import random
import string

# Flask documentation:
# https://flask.palletsprojects.com/en/2.0.x/quickstart/#static-files
app = Flask(__name__)

# documentation to get Flask to support SocketIO:
# https://flask-socketio.readthedocs.io/en/latest/getting_started.html
# app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)


@app.route("/")
def question_page():
    user_cookie = request.cookies.get('userID', default='-1')
    if cookie_exists(user_cookie):
        return render_template("question.html")
    else:
        resp = make_response(render_template("question.html"))
        resp.set_cookie('userID', generate_cookie())
        return resp


@app.route("/scoreboard")
def scoreboard():
    user_cookie = request.cookies.get('userID', default='-1')
    if cookie_exists(user_cookie):
        return render_template("scoreboard.html")
    else:
        resp = make_response(render_template("scoreboard.html"))
        resp.set_cookie('userID', generate_cookie())
        return resp


@app.route("/buttonpress", methods=['POST'])
def button_press():
    print(request)
    request_data_json = request.get_json()
    request_data = json.loads(request_data_json)
    answer = request_data['answer']
    question_id = request_data['qid']
    userID = request.cookies.get('userID', default='-1')
    main.increment("db connection thingy", answer, question_id)

    if question_id == main.mostCommon("db connection thingy", question_id):
        main.updateScore("db connection thingy", 10, userID)


# @socketio.on('answer')
# def button_pressed(data):
#     # Handle the choice for the user
#     print("data from JS: " + str(data))
#     answer = data['data']
#     token = data['uid']
#     question_id = data['qid']
#     db_connection = "connection thingy"
#     main.increment(db_connection, answer, question_id)
#
#     if question_id == main.mostCommon(db_connection, question_id):
#         main.updateScore(db_connection, 10, token)
#     # Emit something for the user to say if they follow the hive or not!
#     # emit('answer_callback', json.dumps({"You are with the hive!"}))
#     emit("answer", {"message" : "you are with the hive"}, json=True)
#
#     print("message should have sent!")
#     pass


# https://pythonbasics.org/flask-cookies/
def cookie_exists(user_cookie):
    if user_cookie == '-1':
        print("no cookie :(")
        return False
    else:
        print("yes cookie :) " + user_cookie)
        return True


# https://pynative.com/python-generate-random-string/#h-steps-to-create-a-random-string
def generate_cookie():
    characters = string.ascii_letters + string.digits
    cookie = ''.join(random.choice(characters) for i in range(100))
    return cookie


if __name__ == '__main__':
    socketio.run(app, debug=True)
