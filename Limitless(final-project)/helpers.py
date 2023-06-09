from functools import wraps
from flask import redirect, render_template, request, session,g
from cs50 import SQL
import sqlite3


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("players.db")
    return g.db

def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def assign_exercise(score, test_name, userid):
    db = get_db()

    # store the current ex programme
    currentProg = db.execute("SELECT exercise FROM players WHERE users_id = ?",(userid,)).fetchall()

    # if there's a slight limitation
    if score == 2:
        while True:
            # choose one exercise for the impaired pattern from the db
            exercises = db.execute("SELECT name FROM exercises WHERE pattern LIKE ? AND difficulty = 'difficult' ORDER BY RANDOM() LIMIT 1", ('%'+test_name+'%',)).fetchone()
            # if it's not empty
            if exercises:
                exercise = exercises[0]
                # if already has some exer in the programm
                if currentProg:
                    print(currentProg)
                    # loop through each item's value
                    for row in currentProg:
                        # if the new ex is = to the old exer
                        if exercise == row[0]:
                            break
                    else:

                        # insert the exercise into players table
                        db.execute ("INSERT INTO players (exercise, repetitions, series, users_id) VALUES (?, 12, 3, ?)", (exercise, userid))
                        break

                else:
                    # insert the exercise into players table
                    db.execute ("INSERT INTO players (exercise, repetitions, series, users_id) VALUES (?, 12, 3, ?)", (exercise, userid))
                    break

    # if there's a more severe limitation
    elif score == 1 or score == 0:


        # select two exercises for that difficulty and that impaired pattern
        exercisesEasy = db.execute("SELECT name FROM exercises WHERE pattern LIKE ? AND difficulty = 'easy' ORDER BY RANDOM()",('%'+test_name+'%',)).fetchone()
        exercisesMid = db.execute("SELECT name FROM exercises WHERE pattern LIKE ? AND difficulty = 'mid' ORDER BY RANDOM()",('%'+test_name+'%',)).fetchone()
        if exercisesEasy and exercisesMid:

            # loop through the tuple containing all the easy exercises for that impaired pattern
            for exerciseEasy in exercisesEasy:
                # loop through the current exercise programm
                if exerciseEasy not in currentProg:

                    db.execute ("INSERT INTO players (exercise, repetitions, series, users_id) VALUES (?, 8, 4, ?)", (exerciseEasy, userid))
                    break

            # loop through the tuple containing all the mid difficulty exercises for that impaired pattern
            for exerciseMid in exercisesMid:
                # loop through the current exercise programm
                if exerciseMid not in currentProg:

                    repetitions = 30 if exerciseMid == 'Brettzel' else 10
                    # insert the exercise in player's db
                    db.execute ("INSERT INTO players (exercise, repetitions, series, users_id) VALUES (?, ?, 3, ?)", (exerciseMid, repetitions, userid))
                    break

    db.commit()

def remove_exercise(userid):
    """ remove past exercises' program """

    db = get_db()
    # store in a variable the exercises program
    row = db.execute("SELECT * FROM players WHERE users_id = ?", (userid,))

    # check if row is empty
    if row is None:
        return
    # if has already an exercise program
    else:
        # remove exercises from players db
        db.execute ("DELETE FROM players WHERE users_id = ?", (userid,))

    db.commit()