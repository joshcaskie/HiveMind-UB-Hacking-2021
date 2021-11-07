from flask import Flask, render_template, request, make_response, url_for
from flask_socketio import SocketIO, emit, send

import main
import json

# https://www.educative.io/edpresso/how-to-generate-a-random-string-in-python
import random
import string
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Flask documentation:
# https://flask.palletsprojects.com/en/2.0.x/quickstart/#static-files
app = Flask(__name__)

# documentation to get Flask to support SocketIO:
# https://flask-socketio.readthedocs.io/en/latest/getting_started.html
# app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

conn_string = os.environ.get("DATABASE")
conn = psycopg2.connect(conn_string)
with conn.cursor() as cur:
    cur.execute("DROP TABLE questions")
    cur.execute("DROP TABLE userinfo")
    conn.commit()
main.makeTables(conn)
conn.close()

@app.route("/")
def question_page():
    conn = psycopg2.connect(conn_string)

    user_cookie = request.cookies.get('userID', default='-1')
    if cookie_exists(user_cookie):

        q_row = main.grabQuestionString(conn)
        q_data = q_row[0]

        print(q_row)

        question = q_data[1]
        id = q_data[2]
        choice1 = q_data[3]
        choice2 = q_data[4]
        choice3 = q_data[5]
        choice4 = q_data[6]

        print(question)
        print(id)
        print(choice1)
        print(choice2)

        # Render
        return render_template("question.html")
    else:

        q_row = main.grabQuestionString(conn)
        q_data = q_row[0]

        print(q_row)

        question = q_data[1]
        id = q_data[2]
        choice1 = q_data[3]
        choice2 = q_data[4]
        choice3 = q_data[5]
        choice4 = q_data[6]

        print(question)
        print(id)
        print(choice1)
        print(choice2)

        # Render
        resp = make_response(render_template("question.html"))

        cookie = generate_cookie()
        print(cookie)
        resp.set_cookie('userID', cookie)

        # Adds user to a table
        main.addNewUser(conn, cookie)

        return resp


@app.route("/scoreboard")
def scoreboard():
    conn = psycopg2.connect(conn_string)
    user_cookie = request.cookies.get('userID', default='-1')
    if cookie_exists(user_cookie):

        conn = psycopg2.connect(conn_string)
        q_rows = main.grabAllUser(conn)
        print(q_rows)

        # q_data = q_row[0]
        #
        # print(q_row)
        #
        # question = q_data[1]
        # id = q_data[2]
        # choice1 = q_data[3]
        # choice2 = q_data[4]
        # choice3 = q_data[5]
        # choice4 = q_data[6]
        #
        # print(question)
        # print(id)
        # print(choice1)
        # print(choice2)

        conn = psycopg2.connect(conn_string)
        rows = main.mostCommon(conn)
        for i in rows:
            print(i)

        return render_template("scoreboard.html")
    else:
        # Render
        resp = make_response(render_template("question.html"))

        cookie = generate_cookie()
        print(cookie)
        resp.set_cookie('userID', cookie)

        # Adds user to a table
        main.addNewUser(conn, cookie)

        return resp


@socketio.on('answer')
def button_pressed(data):
    # Handle the choice for the user
    answer = data['data']
#     question_id = data['qid']
#     main.increment("connection thingy", answer, question_id)

    # Emit something for the user to say if they follow the hive or not!
    # emit('answer_callback', json.dumps({"You are with the hive!"}))
    emit("answer", {"message" : "you are with the hive"}, json=True)

    print("message should have sent!")
    pass


# https://pythonbasics.org/flask-cookies/
def cookie_exists(user_cookie):
    if user_cookie == '-1':
        print("no cookie :(")
        return False
    else:
        print("yes cookie :)")
        return True


# https://pynative.com/python-generate-random-string/#h-steps-to-create-a-random-string
def generate_cookie():
    characters = string.digits + 'abcdef' # + string.ascii_letters

    # e755a045-8127-4ab3-b6b4-5906ca0bb1a1

    cookie = ''.join(random.choice(characters) for i in range(8))
    cookie += '-'
    cookie += ''.join(random.choice(characters) for i in range(4))
    cookie += '-'
    cookie += ''.join(random.choice(characters) for i in range(4))
    cookie += '-'
    cookie += ''.join(random.choice(characters) for i in range(4))
    cookie += '-'
    cookie += ''.join(random.choice(characters) for i in range(12))

    # cookie = 'e755a045-8127-4ab3-b6b4-' + ''.join(random.choice(characters) for i in range(12))
    return cookie


if __name__ == '__main__':
    socketio.run(app, debug=True)
