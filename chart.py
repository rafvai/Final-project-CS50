Multiple Trace Radar Chart


import plotly.graph_objects as go

categories = []
r = []

# Take the names of the tests and save them in a variable
for row in range(len(rows)-2, len(rows)-1):
    current_row = rows[row]
    current_row.pop("id")
    current_row.pop("users_id")
    for key, value in current_row.items():
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

fig.show()


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

    categories = []
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

    #


    return render_template("scores.html", myscores = myscores, name = name, num_rows = num_rows)
