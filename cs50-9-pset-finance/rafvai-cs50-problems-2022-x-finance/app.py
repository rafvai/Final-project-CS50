import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # store userid in a variable
    userid = session["user_id"]

    # store all the data for each stock of the user
    stocks = []
    # show all stocks data for that user
    portfolios = db.execute("SELECT * FROM purchases WHERE users_id = ?", userid)
    for portfolio in portfolios:
        stockInfo = lookup(portfolio["symbol"])
        frontendView = {"name": stockInfo["name"],"shares": portfolio["shares"], "price": stockInfo["price"],"total":stockInfo["price"] * portfolio["shares"]}
        stocks.append(frontendView)

    # total cash of the user
    cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]["cash"]

    # cash plus stocks
    totalcash = cash
    for stock in stocks:
        totalcash += stock["total"]

    return render_template("index.html", stocks = stocks, cash = cash, totalcash = totalcash)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # if via POST
    if request.method == "POST":
        # check if the shares is a number
        if not request.form.get("shares").isnumeric():
            return apology("you must insert a valid amount", 400)

        shares = float(request.form.get("shares"))
        symbol = request.form.get("symbol")

        # if there isn't any symbol
        if not symbol:
            return apology("must provide a symbol", 400)
        elif not lookup(symbol):
            return apology ("symbol not found", 400)
        # if shares is a negative number
        elif shares <= 0:
            return apology ("shares must be a positive number",400)

        # creating variables for stock symbol, number of shares, userid and total of the value owned in portfolio
        userid = session["user_id"]

        # check cash balance in user account
        cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]["cash"]
        # price of the stock
        price = lookup(symbol)["price"]

        # if user cannot afford number of shares
        if cash < price * shares:
            return apology ("You don't have enough cash", 404)

        # calculate the new total cash balance
        cashafter = cash - price * shares

        # update new total in db
        db.execute ("UPDATE users SET cash = ? WHERE id = ?", cashafter,userid)

        # set date in the format supported by sql db
        now = datetime.now().strftime('%Y, %B %d')

        # add purchase to db
        db.execute("INSERT INTO purchases (symbol,price,date,shares,total,users_id) VALUES (?,?,?,?,?,?)",symbol, price, now, shares, price * shares, userid)

        # register into history of transactions
        db.execute("INSERT INTO history(users_id,symbol,price,date,type,shares) VALUES (?,?,?,?,?,?)",userid, symbol, price, now, "BUY", shares)

        return redirect ("/")

    #if via GET
    else:
        # return the form to buy a stock
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # user id
    userid = session["user_id"]
    # create variable to append every row
    tables = []
    # select all transaction for that user
    rows = db.execute("SELECT * FROM history WHERE users_id = ?", userid)
    # loop through each row
    for row in rows:
        # append it
        tables.append(row)

    # render table of history' s trtansactions
    return render_template("history.html", tables = tables)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # user access via POST
    if request.method == "POST":
        # storing in a variable stock's info
        stock = lookup(request.form.get("symbol"))

         # if lookup is not successfull
        if not stock:
            # return error
            return apology("Symbol not found",400)

        # if user submits a valid stock symbol
        return render_template("quoted.html", stock = stock)

    # via GET
    else:
        # show form to request a stock
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # if user access to see the registration form
    if request.method == "POST":
        # check for errors
        # no username
        if not request.form.get("username"):
             return apology("must provide username", 400)

        # no password
        elif not request.form.get("password"):
            return apology("must provide a password", 400)

        # no confirmation ????
        elif not request.form.get("confirmation"):
            return apology("must confirm the password", 400)

        # verify password
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # if username in names
        elif len(db.execute("SELECT * FROM users WHERE username = ?",request.form.get("username"))) != 0:
            return apology("username already taken", 400)

        # insert data into db
        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        # rows
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # open the session for that user
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    # if via GET
    else:
        #redirect to the registration page
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # user request via GET
    if request.method == "GET":
        # user'session
        userid = session["user_id"]
        # store all the shares he owns in a list
        rows = db.execute("SELECT symbol,shares FROM purchases WHERE users_id = ?", userid)
        #render template to sell
        return render_template("sell.html", rows= rows)

    # via POST
    else:
        # checking for errors
        # users doesn't select any stock symbol
        if not request.form.get("symbol"):
            return apology("Must insert a stock symbol", 400)

        # user'session
        userid = session["user_id"]
        # set date in the format supported by sql db
        now = datetime.now().strftime('%Y, %B %d')
        # store all the shares he owns in a list
        rows = db.execute("SELECT symbol,shares FROM purchases WHERE users_id = ?", userid)

        # get the option selected by the user
        SelectedOption = request.form.get("symbol")
        # creating a variable for the number of shares to sell
        sharesToSell = int(request.form.get("shares"))
        # add safety checks
        if sharesToSell < 0:
            return apology("You input a negative number of shares", 400)

        # create a variable to store symbol and how many shares user has of that stock
        StockOwned = {}
        # loop through the stocks in user portfolio
        for row in rows:
            # if the symbol input match with one of the stock
            if row["symbol"] == SelectedOption:
                # shares owned for the symbol input
                StockOwned = row
            # if no stock was found with the selected symbol, return an apology message
            if not StockOwned:
                return apology("You don't owe this stock", 400)

        # if user wants to sell more stocks than those he has
        if StockOwned["shares"] < sharesToSell:
            return apology("You don't have enough shares", 400)

        # take all the live info for that stock
        stock = lookup(SelectedOption)

        # cash in the personal account of the user
        cash = db.execute("SELECT cash FROM users WHERE id = ?", userid)[0]["cash"]

        # update cash in db
        db.execute("UPDATE users SET cash = ? WHERE id = ?",cash + stock["price"] * sharesToSell, userid)
        # update the portfolio for the new number of shares owned and new total?????
        db.execute("UPDATE purchases SET shares = ? WHERE users_id = ? AND symbol = ?",StockOwned["shares"] - sharesToSell, userid, SelectedOption)
        # register into history of transactions
        db.execute("INSERT INTO history(users_id,symbol,price,date,type,shares) VALUES (?,?,?,?,?,?)",userid, SelectedOption, stock["price"], now, "SOLD", sharesToSell)

    # redirect to homepage
    return redirect("/")

@app.route("/add", methods = ["GET", "POST"])
def add():
    """ Add money to portfolio """

    # if via GET show the form to add money
    if request.method == "GET":
        return render_template("add.html")

    # if via POSTf
    else:
        money = request.form.get("money")
        # if money is equal or less than o
        if money <= 0:
            return apology("Please add more money", 406)
        # user'session
        userid = session["user_id"]
        # set date in the format supported by sql db
        now = datetime.now().strftime('%Y, %B %d')

        # update user's cash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", money, userid)

        # INSERT INTO transactions' history
        db.execute("INSERT INTO history (users_id,date,price,type) VALUES(?,?,?,?)", userid,now,money,"RECHARGE")

        return redirect("/")