from lib2to3.pgen2 import token
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from flask_session import Session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)
app.config.from_pyfile('config.cfg')
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

mail = Mail(app)
s = URLSafeTimedSerializer('Thisisasecret!')
ss = URLSafeTimedSerializer('asdqqweasdasd')
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///my_coin.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# @app.route("/", methods=["GET", "POST"])
# @login_required
# def index():
#     return render_template("index.html")
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

@app.route("/wallet")
@login_required
def wallet():
    return render_template("emptywallet.html")
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


@app.route("/statistics")
@login_required
def statistics():
    return render_template("statistics.html")
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

        if rows[0]['confirmed'] == "False":
            return apology(f"you do not confirmed your email {rows[0]['confirmed']}", 400)

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


@app.route("/")
@login_required
def home():
    return render_template("home.html")
    # """Get stock quote."""
    # if request.method == "POST":
    #     stock = lookup(request.form.get("symbol"))
    #     if stock is None:
    #         return apology("Uncorrect symbol", 400)
    #     return render_template("quoted.html", stock=stock)
    # else:
    #     return render_template("quote.html")


name = 0


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
        if db.execute("SELECT username FROM users WHERE username = ?", username):
            return apology("username is already exists", 400)
        else:
            try:
                token = s.dumps(username, salt='email-confirm')

                msg = Message('Confirm Email', sender='mycoinhelp@gmail.com', recipients=[username])

                link = url_for('confirm_email', token=token, _external=True)

                msg.body = 'Your link is {} tap on it to complete registration'.format(link)

                mail.send(msg)

                db.execute("INSERT INTO users(username, hash, confirmed) VALUES(?, ?, 'False')", username,
                generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))
                rows = db.execute("SELECT * FROM users WHERE username = ?", username)
                session["user_id"] = rows[0]["id"]
                global name
                name = username
            except:
                return apology("please enter correct email", 400)
            return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/cashflow")
@login_required
def cashflow():
    return render_template("cashflow.html")
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


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'GET':
#         return '<form action="/" method="POST"><input name="email"><input type="submit"></form>'

#     email = request.form['email']
#     token = s.dumps(email, salt='email-confirm')

#     db.execute("INSERT INTO use (username,confirm)VALUES(?, 'False')", (email,))

#     msg = Message('Confirm Email', sender='my_coin@yahoo.com', recipients=[email])

#     link = url_for('confirm_email', token=token, _external=True)

#     msg.body = 'Your link is {}'.format(link)

#     mail.send(msg)

#     return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    rows = db.execute("SELECT * FROM users WHERE username = ?", name)
    try:
        username = s.loads(token, salt='email-confirm', max_age=3600)
        token = 0
    except SignatureExpired:
        if rows[0]['confirmed'] == "False":
            db.execute("DELETE FROM users WHERE username = ?", name)
        return '<h1>The token is expired!</h1>'
    db.execute("UPDATE users SET confirmed = ? WHERE username = ?", 'True', name)
    return '<h1>Congratulation you have confirmed your email, now you can login into your account</h1>'

user = 0
@app.route("/recovery_password", methods=['GET', 'POST'])
def recovery_password():
    if request.method == "POST":

        email = request.form.get("email")
        if not email:
            return apology("You did not wrote your email", 400)
        global user
        user = email
        # sending token to mail to recover password
        try:

            token = ss.dumps(email, salt='recovery-password')

            msg = Message('Complete Recovery', sender='mycoinhelp@gmail.com', recipients=[email])

            link = url_for('complete_recovery', token=token, _external=True)

            msg.body = 'Your link is {} tap on it to recover the password'.format(link)

            mail.send(msg)
        except:
            return apology("please enter correct email")
        return f"email:{email} token:{token}"
    else:
        return render_template("recovery_password.html")


@app.route("/complete_recovery/<token>", methods=['GET', 'POST'])
def complete_recovery(token):
    if request.method == "POST":
        # changing forgotten password
        db.execute("UPDATE users SET hash = ? WHERE username = ?", generate_password_hash(request.form.get("recoverpassword"), method='pbkdf2:sha256'), user)
        return redirect("/login")
    else:
        try:
            username = ss.loads(token, salt='recovery-password', max_age=3600)
            return render_template("complete_recovery.html")
        except SignatureExpired:
            return '<h1>The token is expired!</h1>'



@app.route("/settings", methods=['GET', 'POST'])
def settings():
    if request.method == "POST":
        # changing password
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if not request.form.get("oldpassword"):
            return apology("must provide oldpassword", 400)
        if not check_password_hash(rows[0]["hash"], request.form.get("oldpassword")):
            return apology("please enter correct password", 400)
        if check_password_hash(rows[0]["hash"], request.form.get("oldpassword")):
            if not request.form.get("newpassword"):
                return apology("must provide newpassword", 400)
            else:
                db.execute("UPDATE users SET hash = ? WHERE id = ?",generate_password_hash(request.form.get("newpassword"), method='pbkdf2:sha256', salt_length=8), session["user_id"])
        return redirect("/login")
    else:
        return render_template("settings.html")


if __name__ == '__main__':
    app.run(debug=True)
