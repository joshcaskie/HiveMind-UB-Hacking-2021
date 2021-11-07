import logging
import os
import psycopg2
import random
import uuid

def makeTables(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS userinfo (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), userAnswer INT, token STRING, score INT)")
        cur.execute("CREATE TABLE IF NOT EXISTS questions (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), question STRING, questionID INT, display1 STRING, display2 STRING, display3 STRING, display4 STRING, answer1 INT, answer2 INT, answer3 INT, answer4 INT)")
        cur.execute("INSERT INTO questions VALUES ('e755a045-8127-4ab3-b6b4-5906ca0bb1a0','Is water wet?', 0, 'yes','no','','',0,0,0,0)")
        cur.execute("INSERT INTO questions VALUES ('e755a045-8127-4ab3-b6b4-5906ca0bb1a1','If the gingerbread man is living in a gingerbread house, is he made out of his house or is his house made out of his skin?', 1, 'he is made out of his house','his house is made out of his skin','','',0,0,0,0)")
        cur.execute("INSERT INTO questions VALUES ('e755a045-8127-4ab3-b6b4-5906ca0bb1a2','Is every food a soup or a sandwich', 2, 'yes','no','','',0,0,0,0)")
        cur.execute("INSERT INTO questions VALUES ('e755a045-8127-4ab3-b6b4-5906ca0bb1a3','which orange came first -- the fruit or the color?', 3, 'fruit','color','','',0,0,0,0)")
        cur.execute("INSERT INTO questions VALUES ('e755a045-8127-4ab3-b6b4-5906ca0bb1a4','what is Ethan Blanton''s last name?', 4, 'Alphonece','Hunt','Hartloff','Ethan',0,0,0,0)")
        conn.commit()

def addNewUser(conn, token):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO userinfo VALUES ('"+token+"', 100, '"+token+"', 0)")
        conn.commit()

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
        cur.execute("SELECT question FROM questions WHERE questionID = " + str(number))
        q = cur.fetchall()
        conn.commit()
        return q[0][0]


# Conn for connection to database, ans is the given answer from the user and the question
def increment(conn, ans, que, token):
    with conn.cursor() as cur:
        # Below would be answer1 - answer 4 based on input
        updatedAnswer = "answer" + str(ans)
        cur.execute("SELECT " + updatedAnswer + " FROM questions")
        rows = cur.fetchall()
        conn.commit()
        ansUpdate = 0
        for row in rows:
            if (row[1] == que):
                ansUpdate += row[6 + (ans - 1)] + 1
        cur.execute("UPDATE questions SET " + updatedAnswer + " = " + ansUpdate)
        cur.execute("UPDATE userinfo SET userAnswer = " + ans + "WHERE token =" + token)
        conn.commmit()


# Returns most common question answer given the question ID
def mostCommon(conn, que):
    with conn.cursor() as cur:
        cur.execute("SELECT answer1,answer2,answer3,answer4 FROM questions")
        rows = cur.fetchall()
        conn.commit()
        for row in rows:
            if (row[1] == que):
                max1 = max(row[6], row[7])
                max2 = max(max1, row[8])
                return max(max2, row[9])


# Update user score given their score to be added and their unique token.
def updateScore(conn, score, token):
    with conn.cursor() as cur:
        cur.execute("SELECT score FROM userinfo WHERE token = " + token)
        rows = cur.fetchall()
        updatedScore = (rows[2] + score)
        cur.execute("UPDATE userinfo SET score = " + updatedScore + " WHERE token = " + token)
        conn.commit()


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




