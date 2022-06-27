import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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
db = SQL("sqlite:///my_coin.db")

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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # if request.method == "POST":
    #     money = request.form.get("money")
    #     cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    #     moneys = int(money) + cash[0]["cash"]
    #     db.execute("UPDATE users SET cash = ? WHERE id = ?", moneys, session["user_id"])
    #     return redirect("/")

    # else:
    #     """Show portfolio of stocks"""
    #     rows = db.execute("SELECT * FROM purchases WHERE purchase_id = ?", session["user_id"])
    #     count = db.execute("SELECT COUNT(purchase_id) FROM purchases WHERE purchase_id = ?", session["user_id"])
    #     Count = count[0]['COUNT(purchase_id)']
    #     cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    #     if not rows:
    #         return render_template("emptyindex.html",cash=cash)
    #     for i in range(Count):
    #         symb = []
    #         symbol = rows[i]["symbol"]
    #         if symbol in symb:
    #             continue
    #         stocks = lookup(symbol)
    #         name = stocks["name"]
    #         share = db.execute("SELECT sum(shares) FROM purchases WHERE symbol = ? and purchase_id = ?", symbol, session["user_id"])
    #         shares = share[0]['sum(shares)']
    #         price = stocks["price"]
    #         total = "%0.2f" % (price * int(shares))
    #         cashes = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    #         cash = cashes[0]["cash"]
    #         symb.append(symbol)
    #         db.execute("DELETE FROM sumpurchases WHERE sumpurchase_id = ? and symbol = ?", session["user_id"], symbol)
    #         db.execute("INSERT INTO sumpurchases(sumpurchase_id,symbol,name,shares,price,total)VALUES(?,?,?,?,?,?)", session["user_id"], symbol, name, shares, price, total)
    #         TOTAL = db.execute("SELECT sum(total) FROM sumpurchases WHERE sumpurchase_id = ?", session["user_id"])
    #         Total = TOTAL[0]["sum(total)"] + cash
    #         sumpurchases = db.execute("SELECT * FROM sumpurchases WHERE sumpurchase_id = ?", session["user_id"])
    #     try:
    #         return render_template("index.html", sumpurchases=sumpurchases, cash=cash, TOTAL=Total)
    #     except TypeError:
    #         return redirect("/")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # """Buy shares of stock"""
    # if request.method == "POST":
    #     symbol = request.form.get("symbol")
    #     stocks = lookup(request.form.get("symbol"))
    #     if not symbol or stocks is None:
    #         return apology("symbol is blank or the symbol does not exist", 400)
    #     shares = request.form.get("shares")
    #     if not shares or shares is None or not shares.isdigit() or int(shares) <= 0:
    #         return apology("you do not write a number of shares", 400)
    #     money = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    #     price = stocks['price']
    #     name = stocks['name']
    #     change = money[0]["cash"] - (price * float(shares))
    #     if change < 0:
    #         return apology("you does not have money to buy",400)
    #     db.execute("INSERT INTO purchases(purchase_id,symbol,name,shares,price)VALUES(?,?,?,?,?)", session["user_id"], stocks['symbol'], name, shares, price)
    #     db.execute("INSERT INTO buy(buy_id,symbol,shares,price)VALUES(?,?,?,?)", session["user_id"], symbol, shares, price)
    #     db.execute("UPDATE users SET cash = ? WHERE id = ?", change, session["user_id"])
    #     return redirect("/")
    # else:
    #     return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    # """Show history of transactions"""
    # buy = db.execute("SELECT * FROM buy WHERE buy_id = ? ORDER BY daytime DESC", session["user_id"])
    # sell = db.execute("SELECT * FROM sell WHERE sell_id = ? ORDER BY daytime DESC", session["user_id"])
    # return render_template("history.html", buy=buy, sell=sell)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

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
    # """Get stock quote."""
    # if request.method == "POST":
    #     stock = lookup(request.form.get("symbol"))
    #     if stock is None:
    #         return apology("Uncorrect symbol", 400)
    #     return render_template("quoted.html", stock=stock)
    # else:
    #     return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return apology("You did not wrote your username", 400)
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation or password != confirmation:
            return apology("different passwords", 400)
        if db.execute("SELECT username FROM users WHERE username = ?", request.form.get("username")):
            return apology("username is already exists", 400)
        else:
            db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", username, generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
            session["user_id"] = rows[0]["id"]
            return redirect("/")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # """Sell shares of stock"""
    # if request.method == "POST":
    #     symbol = request.form.get("symbol")
    #     stocks = lookup(request.form.get("symbol"))
    #     if not symbol or stocks is None:
    #         return apology("symbol is blank or the symbol does not exist", 400)
    #     purchase = db.execute("SELECT symbol,sum(shares) FROM purchases WHERE purchase_id = ? and symbol = ?", session["user_id"], symbol)
    #     symbol1 = purchase[0]["symbol"]
    #     if not symbol1:
    #         return apology("You does not have a shares of this company", 400)
    #     name = stocks['name']
    #     shares = request.form.get("shares")
    #     shares1 = purchase[0]["sum(shares)"]
    #     if shares1 < int(shares):
    #         return apology(f"You does not have {shares} shares of this company", 400)
    #     stonks = shares1 - int(shares)
    #     price = stocks['price']
    #     db.execute("DELETE FROM purchases WHERE purchase_id = ? and symbol = ?", session["user_id"], symbol)
    #     db.execute("INSERT INTO purchases(purchase_id,symbol,name,shares,price)VALUES(?,?,?,?,?)", session["user_id"], symbol, name, stonks, price)
    #     db.execute("UPDATE sumpurchases SET shares = ? WHERE sumpurchase_id = ? and symbol = ?", stonks, session["user_id"], symbol)
    #     profit = int(shares) * price
    #     cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    #     profit1 = profit + cash[0]["cash"]
    #     db.execute("INSERT INTO sell(sell_id,symbol,shares,price)VALUES(?,?,?,?)", session["user_id"], symbol, shares, price)
    #     db.execute("UPDATE users SET cash = ? WHERE id = ?", profit1, session["user_id"])
    #     db.execute("DELETE FROM purchases WHERE shares = '0' and purchase_id = ? and symbol = ?", session["user_id"], symbol)
    #     db.execute("DELETE FROM sumpurchases WHERE shares = '0' and sumpurchase_id = ? and symbol = ?", session["user_id"], symbol)
    #     return redirect("/")
    # else:
    #     sumpurchases = db.execute("SELECT * FROM sumpurchases WHERE sumpurchase_id = ?", session["user_id"])
    #     return render_template("sell.html",sumpurchases=sumpurchases )
