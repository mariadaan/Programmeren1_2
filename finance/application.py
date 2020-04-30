"""
Problem Set 7
Name: Maria Daan
Student Number: 11243406
"""

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Ensure environment variable is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show index of stocks"""

    dicts_list = []
    summed = 0

    # Query database for grouped stocks
    indexed = db.execute("SELECT * FROM index_table WHERE id = :id",
                         id=session["user_id"])

    # Append info about each stock into dictionaries in a list
    for stock in indexed:
        symbol = stock["Symbol"]
        info = lookup(symbol)
        symbolname = info["name"]
        shares = stock["Shares"]
        price = info["price"]
        total = float(price) * float(shares)
        summed += float(total)
        stock_dict = {
            "symbol": symbol,
            "symbolname": symbolname,
            "shares": shares,
            "price": usd(price),
            "total": usd(total)}
        dicts_list.append(stock_dict)

    # Query database for cash
    cash = db.execute("SELECT cash FROM users WHERE id = :id",
                      id=session["user_id"])

    # Calculate user's total cash
    summed += float(cash[0]["cash"])

    # Show the user all buys and current values
    return render_template("index.html",
                           dicts=dicts_list,
                           cash=usd(cash[0]["cash"]),
                           TOTAL=usd(summed))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure (valid) symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)
        elif lookup(request.form.get("symbol")) == None:
            return apology("invalid symbol")

        # Ensure (valid) share was submitted
        if not request.form.get("shares"):
            return apology("missing share", 400)
        elif not request.form.get("shares").isdigit():
            return apology("share must be an integer number", 400)
        elif int(request.form.get("shares")) < 1:
            return apology("share must be positive", 400)

        # Check if user can afford it
        user_cash = db.execute("SELECT cash FROM users WHERE id = :id",
                               id=session["user_id"])
        stock = lookup(request.form.get("symbol"))
        totalprice = float(stock["price"]) * float(request.form.get("shares"))

        if float(totalprice) > float(user_cash[0]["cash"]):
            return apology("can't afford", 400)

        # Add stock to portfolio
        db.execute("INSERT INTO portfolio (id,Stock,Price, Share)\
                    VALUES (:id,:symbol,:price,:shares)",
                   id=session["user_id"],
                   symbol=stock["symbol"],
                   price=stock["price"],
                   shares=request.form.get("shares"))

        # Check if stock is owned already
        if len(db.execute("SELECT Symbol FROM index_table \
                        WHERE Symbol = :symbol AND id = :id",
                          id=session["user_id"],
                          symbol=stock["symbol"])) == 0:

            # Add stock to index if stock isn't owned already
            db.execute("INSERT INTO index_table (id,Symbol,Shares,Price,Total)\
                        VALUES (:id,:symbol,:shares,:price,:total)",
                       id=session["user_id"],
                       symbol=stock["symbol"],
                       shares=request.form.get("shares"),
                       price=stock["price"],
                       total=totalprice)
        else:
            # Update shares
            db.execute("UPDATE index_table SET Shares = Shares + :shares\
                        WHERE Symbol = :symbol AND id = :id",
                       id=session["user_id"],
                       symbol=stock["symbol"],
                       shares=int(request.form.get("shares")))

        # Update user's cash
        db.execute("UPDATE users SET cash = cash - :totalprice WHERE id = :id",
                   totalprice=float(totalprice),
                   id=session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Select needed elements from portfolio
    data = db.execute("SELECT * FROM portfolio WHERE id = :id",
                      id=session["user_id"])

    # Convert price to USD format
    for item in data:
        item["Price"] = usd(item["Price"])

    # Show the user all buys and sells
    return render_template("history.html",
                           dicts=data)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure (valid) symbol was submitted
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)
        elif lookup(request.form.get("symbol")) == None:
            return apology("invalid symbol")

        quote = lookup(request.form.get("symbol"))

        # Send quote's price, symbol and name to "quoted" template
        return render_template("quoted.html",
                               price=usd(quote["price"]),
                               name=quote["name"],
                               symbol=quote["symbol"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # PERSONAL TOUCH: require passwords to have special characters
        # and to be different from the username
        elif request.form.get("password").isalpha():
            return apology("password must provide special character", 400)
        elif request.form.get("password") == request.form.get("username"):
            return apology("password and username can't be the same", 400)

        # Confirm password
        elif not request.form.get("confirmation"):
            return apology("must provide password again", 400)
        elif not request.form.get("confirmation") == request.form.get("password"):
            return apology("passwords do not match", 400)

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username doesn't already exist
        if len(rows) != 0:
            return apology("username already exists", 400)

        # Add user to database
        db.execute("INSERT INTO users (username,hash) VALUES(:username, :password)",
                   username=request.form.get("username"),
                   password=generate_password_hash(request.form.get("password")))

        new = db.execute("SELECT * FROM users WHERE username = :username",
                         username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = new[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        share = db.execute("SELECT Shares FROM index_table WHERE id = :id AND Symbol = :symbol",
                           id=session["user_id"],
                           symbol=request.form.get("symbol"))

        # Ensure (valid) share was submitted
        if not request.form.get("shares"):
            return apology("missing share", 400)
        elif not request.form.get("shares").isdigit():
            return apology("share must be an integer number", 400)
        elif int(request.form.get("shares")) < 1:
            return apology("share must be positive", 400)
        elif int(request.form.get("shares")) > int(share[0]["Shares"]):
            return apology("you don't have enough shares", 400)

        # Update amount of shares
        db.execute("UPDATE index_table SET Shares = Shares - :shares WHERE id = :id AND Symbol = :symbol",
                   id=session["user_id"],
                   shares=request.form.get("shares"),
                   symbol=request.form.get("symbol"))

        # Delete row if there are no shares left
        db.execute("DELETE FROM index_table WHERE Shares = 0")

        stock = lookup(request.form.get("symbol"))

        # Save transaction in portfolio
        db.execute("INSERT INTO portfolio (id,Stock,Price, Share) VALUES (:id,:symbol,:price,:shares)",
                   id=session["user_id"],
                   symbol=stock["symbol"],
                   price=stock["price"],
                   shares=int(request.form.get("shares"))*-1)

        totalprice = float(request.form.get("shares"))*float(stock["price"])

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + :totalprice WHERE id = :id",
                   totalprice=float(totalprice),
                   id=session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        symbol_list = []
        stock_list = db.execute("SELECT Stock FROM portfolio WHERE id = :id GROUP BY Stock",
                                id=session["user_id"])

        # Create list of symbols that the user possesses
        for stock in stock_list:
            symbol_list.append(stock["Stock"])

        return render_template("sell.html",
                               symbol_list=symbol_list)


@app.route("/results")
@login_required
def results():
    """PERSONAL TOUCH: Show user how much profit or loss has been made"""

    # Query database for sells, buys and current values
    sells = db.execute("SELECT Stock, Price, Share, SUM(Price*-Share) AS Summed FROM portfolio WHERE id = :id AND Share < 0 GROUP BY Stock",
                       id=session["user_id"])
    buys = db.execute("SELECT Stock, Price, Share, SUM(Price*Share) AS Summed FROM portfolio WHERE id = :id AND Share > 0 GROUP BY Stock",
                      id=session["user_id"])
    currents = db.execute("SELECT Symbol, Shares FROM index_table WHERE id = :id",
                          id=session["user_id"])

    total_sells = 0
    total_buys = 0
    current_value = 0
    final = ""

    # Sum the earnings
    for stock in sells:
        total_sells += stock["Summed"]

    # Sum the expenses
    for stock in buys:
        total_buys += stock["Summed"]

    # Calculate the current value of holdings
    for stock in currents:
        symbol = lookup(stock["Symbol"])
        cur_price = symbol["price"] * stock["Shares"]
        current_value += cur_price

    # Calculate the total profit/loss
    total_profit = total_sells - total_buys + current_value

    # Format string to tell user the profit/loss
    if total_profit > 0:
        final = f"You have earned {usd(total_profit)}."
    else:
        final = f"You have lost {usd(total_profit * -1)}."

    # Redirect user to results page
    return render_template("results.html",
                           total_sells=usd(total_sells),
                           total_buys=usd(total_buys),
                           current_value=usd(current_value),
                           total_profit=usd(total_profit),
                           final=final)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
