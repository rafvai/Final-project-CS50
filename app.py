from cs50 import SQL
from flask import Flask, flash, render_template, request, session, redirect
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, assign_exercise, remove_exercise
from datetime import datetime
import json
import plotly.graph_objects as go



# configure application
app = Flask(__name__)

# configure database
db = SQL("sqlite:///players.db")

# configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# define homepage
@app.route("/")
@login_required
def index():
    """ Shows exercises for that player """

    # store the userID into a variable
    userid = session["user_id"]

    # create a variable to be passed to frontend containing all exercises
    exercises = []

    # select and store into a dict all the exercises for that player
    rows = db.execute("SELECT * FROM players WHERE users_id = ?", userid)
    # loop through all exercises
    for row in rows:
        # loop through each info of that exercise
        row.pop("users_id")
        # append them to be passed into frontend
        exercises.append(row)

    # save full name of the player
    name = db.execute("SELECT name FROM users WHERE id = ?", userid)[0]["name"]
    lastname = db.execute("SELECT lastname FROM users WHERE id = ?", userid)[0]["lastname"]

    return render_template("index.html", exercises = exercises, name = name, lastname = lastname)



# define the login
@app.route("/login", methods = ["GET", "POST"])
def login():
    """ Allow user to log in """
    # forget user id
    session.clear()

    # if user accesses via get
    if request.method == "GET":
        # return the login page
        return render_template("login.html")
    # if submits the form
    else:
        # checking for errors
        # user didn't input the username
        if not request.form.get("username"):
            return ("Must input a valid username", 403)

        # if didn't input password
        elif not request.form.get("password"):
            return ("Must input a password", 403)

        # access to db to retrieve username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # ensure username exists
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return ("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



# define register route
@app.route("/register", methods = ["GET", "POST"])
def register():
    """ Show the registration form """

    # user access submitting a form
    if request.method == "POST":
        # checking for errors
        # if user doesn't submit a name
        if not request.form.get("name"):
            return ("Must insert name", 400)

        #if user doesn't submit a last name
        elif not request.form.get("lastname"):
            return ("Must insert a lastname", 400)

        # if doesn't submit username
        elif not request.form.get("username"):
            return ("Must insert a valid username", 400)

        # if doesn't input a password
        elif not request.form.get("password"):
            return ("Must insert a valid password", 400)

        # if doesn't input a confirmation
        elif not request.form.get("confirmation"):
            return ("Must insert a valid confirmation password", 400)

        # if password doesn't match confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return ("Passwords don't match", 400)

        # check if username already taken
        elif len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))) != 0:
            return ("Username already in use", 400)

        # insert into db
        db.execute("INSERT INTO users(name, lastname,username, hash) VALUES(?,?,?,?)",request.form.get("name"),request.form.get("lastname"), request.form.get("username"), generate_password_hash(request.form.get("password")))

        # open the session for that user
        userId = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))[0]["id"]

        session["user_id"] = userId

        # Redirect user to home page
        return redirect("/")

    # if users reaches it via get
    else:
        return render_template("register.html")



@app.route("/scores", methods = ["GET"])
@login_required
def scores():
    """ Show all my assessments and a graphical representation of them """

    # store user's id
    userid = session["user_id"]
    # store user's name
    name = db.execute("SELECT name FROM users WHERE id = ?", userid)[0]["name"]
    # create a list to store data to be passed to frontend
    myscores = []
    # store all the results for that user in a variable
    rows = db.execute("SELECT * FROM scores WHERE users_id = ?", userid)

    # loop through the table and save only the scores in the variable for frontend
    for row in rows:
        row.pop("id")
        # Remove the "users_id" key from the dictionary
        row.pop("users_id")
        # Create a new dictionary to store the modified key-value pairs
        new_row = {}
        for key, value in row.items():
            new_key = key.replace("_", " ")
            new_row[new_key] = value
        # Append the modified dictionary to myscores
        myscores.append(new_row)

    # calculate the length of myscores
    num_rows = len(myscores)

    categories = []
    r = []

    # Take the names of the tests and save them in a variable
    for row in myscores[num_rows - 2: num_rows - 1]:
        for key, value in row.items():
            categories.append(key)
            r.append(value)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=r,
        theta=categories,
        fill='toself',
        name='Product A'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3]
            )
        ),
        showlegend=False
    )

    fig_json = fig.to_json()

    return render_template("scores.html", myscores = myscores, name = name, num_rows = num_rows, fig_json=fig_json)



@app.route("/add", methods = ["GET", "POST"])
@login_required
def add():
    """ Section to add a new patient """

    # if user accesses via get
    if request.method == "GET":

        # store the userID into a variable
        userid = session["user_id"]
        # create variables to pass to frontend the possible scores and the name of tests
        scores = [0, 1, 2, 3]
        tests = ['deep squat','hurdle step','in line lunge','shoulder mobility','active straight leg raise','trunk stability push up','rotary stability']

        return render_template("add.html", scores = scores, tests = tests)

    # if user submits data
    else:

        # store today's date in a variable
        today = datetime.now().strftime('%d %b %Y')
        # store test's names
        test_names = ['deep squat','hurdle step','in line lunge','shoulder mobility','active straight leg raise','trunk stability push up','rotary stability']
        # create a list of dict to store key and results obtained by user
        test_scores = []
        # user id
        userid = session["user_id"]
        # loop through test's names
        for key in test_names:
            # take the score
            score = { key: int(request.form.get(key))}
            # add key and score to the variable
            test_scores.append(score)

        # insert a new row in the table
        db.execute("INSERT INTO scores(users_id, date) VALUES (?, ?)", userid, today)

        # remove previous exercises program
        remove_exercise(userid)

        # loop through scores
        for score in test_scores:
            for key, value in score.items():
                key = key.replace(" ","_")
                # add results to db
                db.execute("UPDATE scores SET ? = ? WHERE users_id = ? AND date = ?",key, value, userid, today)

                # assign specific exercises according to test's scores
                assign_exercise(value, key ,userid)

    return redirect("/")


@app.route("/tests", methods = ["GET", "POST"])
def tests():
    """ Show tests and allow to select them to get more information """

    # if user doesn't submit data
    if request.method == "GET":

        # create a variable to store test's names
        names = []

        # store column's names
        tests = db.execute("SELECT * FROM scores")[0]
        # take all column's names except users_id and date
        tests.pop("id")
        tests.pop("users_id")
        tests.pop("date")

        for key in tests.keys():
            key = key.replace("_"," ")
            names.append(key)

        return render_template("tests.html", names = names)

    else:
        # take test's name that user input
        testName = request.form.get("tests")
        # look into db to find the description of the selected test(format it in db column's names)
        testDescription = db.execute("SELECT test_description FROM tests_explained WHERE test_name LIKE ? ", testName.replace(" ", "_"))[0]["test_description"]

        return render_template("tests_explained.html", testName = testName, testDescription = testDescription)



@app.route("/exercises", methods = ["GET"])
@login_required
def exercises():
    """ Show the current gallery of exercises specific for the athlete """

    # create a list to store exercises' name
    exercises = []

    userid = session["user_id"]

    # access db to retrive the exercises'name for that player
    rows = db.execute("SELECT name, set_up, action, return, starting_position, pattern, link FROM exercises JOIN players ON exercises.name = players.exercise WHERE users_id = ? ",userid)
    # iterate through each exercise and store its formatted info into variable exercises
    for row in rows:
        exerciseInfo = {}
        # iterate through each key of that exercise
        for key,value in row.items():
            # format the key to be passed to frontend
            if key == "set_up" or key == "starting_position":
                key = key.replace("_"," ")
            exerciseInfo[key] = value
            # append it
        exercises.append(exerciseInfo)

    return render_template("exercises.html", exercises = exercises)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
