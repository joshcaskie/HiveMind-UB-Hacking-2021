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

users = {}

@app.route("/")
def question_page():

    user_cookie = request.cookies.get('userID', default='-1')
    if cookie_exists(user_cookie):

        conn = psycopg2.connect(conn_string)
        q_row = main.grabQuestionString(conn)
        q_data = q_row[0]

        question = q_data[1]
        id = q_data[2]
        choice1 = q_data[3]
        choice2 = q_data[4]
        choice3 = q_data[5]
        choice4 = q_data[6]

        # Save locally
        if user_cookie not in users:
            users[user_cookie] = {}

        # Render
        return render_template("question.html", question=question, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4, que=id, cookie=user_cookie)
    else:
        conn = psycopg2.connect(conn_string)
        q_row = main.grabQuestionString(conn)
        q_data = q_row[0]

        question = q_data[1]
        id = q_data[2]
        choice1 = q_data[3]
        choice2 = q_data[4]
        choice3 = q_data[5]
        choice4 = q_data[6]

        # Render
        cookie = generate_cookie()
        resp = make_response(render_template("question.html", question=question, choice1=choice1, choice2=choice2, choice3=choice3, choice4=choice4, que=id, cookie=cookie))

        # print(cookie)
        resp.set_cookie('userID', cookie)

        # Adds user to a table
        conn = psycopg2.connect(conn_string)
        main.addNewUser(conn, cookie)

        # Save locally
        if cookie not in users:
            users[cookie] = {}

        return resp

# This doesn't need to ADD cookies to template; it can generate stuff on post request
@app.route("/scoreboard")
def scoreboard():
    conn = psycopg2.connect(conn_string)
    user_cookie = request.cookies.get('userID', default='-1')
    if cookie_exists(user_cookie):

        # conn = psycopg2.connect(conn_string)
        # q_rows = main.grabAllUser(conn)
        # print(q_rows)

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

            question = i[1]
            choice1 = i[3]
            choice2 = i[4]
            choice3 = i[5]
            choice4 = i[6]
            num1 = i[7]
            num2 = i[8]
            num3 = i[9]
            num4 = i[10]

            # print(num1)
            # print(num2)
            # print(num3)
            # print(num4)

        # Save locally
        if user_cookie not in users:
            users[user_cookie] = {}

        # print(user_cookie)
        answers = users[user_cookie]
        print(answers)
        to_template = {}

        for (que, ans) in answers.items():
            conn = psycopg2.connect(conn_string)
            q = main.grabSpecificQ(conn, que)

            # print("HELELELELELELE\n")
            # print(q)
            # print(2+int(ans))

            to_template[q[0][1]] = q[0][2+int(ans)]
            # print(q[0])

        print(to_template)

        return render_template("scoreboard.html", rows=rows, to_template=to_template)
    else:
        # Render (if no cookie, obviously no scores)
        resp = make_response(render_template("question.html"))

        cookie = generate_cookie()
        print(cookie)
        resp.set_cookie('userID', cookie)

        # Adds user to a table
        conn = psycopg2.connect(conn_string)
        main.addNewUser(conn, cookie)

        # Save locally
        if cookie not in users:
            users[cookie] = {}

        return resp


@socketio.on('answer')
def button_pressed(data):
    print(data)
    # Handle the choice for the user
    answer = data['data']
    que = data['que']
    cookie = data['cookie']
#     question_id = data['qid']
#     main.increment("connection thingy", answer, question_id)

    if int(answer) < 1 or int(answer) > 4:
        emit("answer", {"message": "Nice try :)"}, json=True)
        return

    # Emit something for the user to say if they follow the hive or not!
    # emit('answer_callback', json.dumps({"You are with the hive!"}))

    # Save the user did stuff
    # If the que is already in the users thing, return
    if cookie in users and que in users[cookie]:
        emit("answer", {"message" : "You've already answered this!"}, json=True)
        return
    else:
        users[cookie][que] = answer
        emit("answer", {"message" : "You successfully answered!"})
        conn = psycopg2.connect(conn_string)
        main.increment(conn, int(answer), int(que), "n/a")

    # emit("answer", {"message" : "you are with the hive"}, json=True)


    # conn = psycopg2.connect(conn_string)
    # Perhaps revist, try token, try anything? It's supposed to emit if the user was "right or wrong"

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
