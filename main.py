import logging
import os
import psycopg2
import random
import uuid


def makeTables(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS userinfo (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), userAnswer INT, token STRING, score INT)")
        cur.execute(
            "CREATE TABLE IF NOT EXISTS questions (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), question STRING, questionID INT, display1 STRING, display2 STRING, display3 STRING, display4 STRING, answer1 INT, answer2 INT, answer3 INT, answer4 INT)")
        cur.execute(
            "INSERT INTO questions VALUES ('e755a045-8127-4ab3-b6b4-5906ca0bb1a0','Is water wet?', 0, 'yes','no','','',0,0,0,0)")
        cur.execute(
            "INSERT INTO questions VALUES ('e755a045-8127-4ab3-b6b4-5906ca0bb1a1','If the gingerbread man is living in a gingerbread house, is he made out of his house or is his house made out of his skin?', 1, 'he is made out of his house','his house is made out of his skin','','',0,0,0,0)")
        cur.execute(
            "INSERT INTO questions VALUES ('e755a045-8127-4ab3-b6b4-5906ca0bb1a2','Is every food a soup or a sandwich', 2, 'yes','no','','',0,0,0,0)")
        cur.execute(
            "INSERT INTO questions VALUES ('e755a045-8127-4ab3-b6b4-5906ca0bb1a3','Which orange came first -- the fruit or the color?', 3, 'fruit','color','','',0,0,0,0)")
        cur.execute(
            "INSERT INTO questions VALUES ('e755a045-8127-4ab3-b6b4-5906ca0bb1a4','What is Ethan Blanton''s last name?', 4, 'Alphonce','Hunt','Hartloff','Ethan',0,0,0,0)")
        conn.commit()


def addNewUser(conn, token):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO userinfo VALUES ('" + token + "', 100, '" + token + "', 0)")
        conn.commit()

        cur.execute("SELECT * FROM userinfo")
        stuff = cur.fetchall()
        print("hi")
        print(stuff)

    conn.close()


def grabQuestionString(conn):
    # with conn.cursor() as cur:
    #     cur.execute("SELECT question FROM questions")
    #     logging.debug("print_hello(): status test: %s", cur.statusmessage)
    #     rows = cur.fetchall()
    #     conn.commit()
    #     number = random.randint(0, 4)
    #     print(list(rows[1]))
    #     for row in len(list(rows[1])):
    #         print(row)
    #         # check question id of current row, return the string if number chosen
    #         if rows[1][row] == number:
    #             return row[0][row]
    #     return "no"
    number = random.randint(0, 4)
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM questions WHERE questionID = " + str(number))
        q = cur.fetchall()
        conn.commit()
        return q



def grabSpecificQ(conn, number):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM questions WHERE questionID = " + str(number))
        q = cur.fetchall()
        conn.commit()
        return q


# Conn for connection to database, ans is the given answer from the user and the question
def increment(conn, ans, que, cookie):
    if (ans != 1 and ans != 2 and ans != 3 and ans != 4):
        conn.close()
        return

    with conn.cursor() as cur:
        # Below would be answer1 - answer 4 based on input
        cur.execute("SELECT * FROM questions WHERE questionID = " + str(que))
        row = cur.fetchall()
        conn.commit()
        col = "answer" + str(ans)
        current = row[0][6 + ans]
        cur.execute("UPDATE questions SET " + col + " = " + str(current + 1) + " WHERE questionID =" + str(que))
        print(str(ans))
        # saves that the user answered the question
        print(ans)
        #cookie = "ajkbdieugdfosugfd"
        cur.execute("SELECT token FROM userInfo")
        token = cur.fetchall()
        #temp = 'e755a045-8127-49b3-b6b4-5906ca0bb1a0'
        print(token)
        # if (cookie in token):
        #     cur.execute("UPDATE userinfo SET userAnswer = " + str(ans) + " WHERE EXISTS token = " + cookie)
        # else:
        #     cur.execute("INSERT INTO userinfo VALUES (" + cookie + ", " + str(ans) + ", " + cookie + ", 0)")
        # cur.execute("SELECT * FROM userinfo")
        # stuff = cur.fetchall()
        # print(stuff)
        conn.commit()


# Returns most common question answer given the question ID
def mostCommon(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM questions")
        rows = cur.fetchall()
        conn.commit()
    conn.close()
    return rows


# Update user score given their score to be added and their unique token.
def updateScore(conn, token):
    with conn.cursor() as cur:
        cur.execute("SELECT score FROM userinfo WHERE token = " + token)
        rows = cur.fetchall()
        updatedScore = (rows[2] + 1)
        cur.execute("UPDATE userinfo SET score = " + str(updatedScore) + " WHERE token = " + token)
        conn.commit()


def grabAllUser(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM userinfo")
        rows = cur.fetchall()
        conn.commit()

    conn.close()
    return rows


def main():
    conn_string = input('Enter a connection string:\n')

    conn = psycopg2.connect(os.path.expandvars(conn_string))
    # with conn.cursor() as cur:
    #     cur.execute("DROP TABLE questions")
    #     cur.execute("DROP TABLE userinfo")
    #     conn.commit()
    makeTables(conn)
    with conn.cursor() as cur:
        cur.execute("DROP TABLE questions")
        cur.execute("DROP TABLE userinfo")
        conn.commit()
    # Close communication with the database.fff
    conn.close()


if __name__ == "__main__":
    main()
