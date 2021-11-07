import logging
import os
import psycopg2
import random


def grabQuestionString(conn):
    # with conn.cursor() as cur:
    #     cur.execute("SELECT question FROM questions")
    #     logging.debug("print_hello(): status test: %s", cur.statusmessage)
    #     rows = cur.fetchall()
    #     conn.commit()
    #     number = random.randint(0, 4)
    #     for row in rows:
    #         # check question id of current row, return the string if number chosen
    #         if row[1] == number:
    #             return row[0]
    #     return "no"
    number = random.randint(0, 4)
    with conn.cursor() as cur:
        cur.execute("SELECT question FROM questions WHERE questionID = " + str(number))
        q = cur.fetchall()
        return q[0]


# Conn for connection to database, ans is the given answer from the user and the question
def increment(conn, ans, que):
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
        cur.execute("UPDATE questions SET userAnswer = " + ans)
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
    grabQuestionString(conn)

    # Close communication with the database.
    conn.close()


if __name__ == "__main__":
    main()
