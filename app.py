from cs50 import SQL
from flask import Flask, redirect, render_template, request, session, url_for
from flask_mail import Mail, Message
from flask_session import Session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, exchange_rate
import json
import requests
# Configure application
app = Flask(__name__)
app.config.from_pyfile('config.cfg')
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

mail = Mail(app)
s = URLSafeTimedSerializer('Thisisasecret!')
ss = URLSafeTimedSerializer('asdqqweasdasd')
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = True
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


@app.route("/wallet", methods=["GET", "POST"])
@login_required
def wallet():
    if request.method == "POST":
        uah_income = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'income' and cashflow_id = ? and currency = 'uah'", session["user_id"])[0]["sum(count)"]
        usd_income = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'income' and cashflow_id = ? and currency = 'usd'", session["user_id"])[0]["sum(count)"]
        eur_income = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'income' and cashflow_id = ? and currency = 'eur'", session["user_id"])[0]["sum(count)"]
        uah_expence = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'expense' and cashflow_id = ? and currency = 'uah'", session["user_id"])[0]["sum(count)"]
        usd_expence = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'expense' and cashflow_id = ? and currency = 'usd'", session["user_id"])[0]["sum(count)"]
        eur_expence = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'expense' and cashflow_id = ? and currency = 'eur'", session["user_id"])[0]["sum(count)"]
        if uah_income is None:
            uah_income = 0
        if usd_income is None:
            usd_income = 0
        if eur_income is None:
            eur_income = 0
        if uah_expence is None:
            uah_expence = 0
        if usd_expence is None:
            usd_expence = 0
        if eur_expence is None:
            eur_expence = 0
        cash_uah = uah_income - uah_expence
        cash_usd = usd_income - usd_expence
        cash_eur = eur_income - eur_expence
        currency = request.form.get("currency")
        if currency == "UAH":
            usd_to_uah = exchange_rate["usd_to_uah"]
            eur_to_uah = exchange_rate["eur_to_uah"]
            cash_usd_in_uah = int(cash_usd) * usd_to_uah
            cash_usd_in_uah = float(round(cash_usd_in_uah, 2))
            cash_eur_in_uah = int(cash_eur) * eur_to_uah
            cash_eur_in_uah = float(round(cash_eur_in_uah, 2))
            cash_uah = float(round(cash_uah, 2))
            money = cash_usd_in_uah + cash_eur_in_uah + float(cash_uah)
        elif currency == "USD":
            uah_to_usd = exchange_rate["uah_to_usd"]
            eur_to_usd = exchange_rate["eur_to_usd"]
            cash_uah_in_usd = int(cash_uah) * uah_to_usd
            cash_uah_in_usd = float(round(cash_uah_in_usd, 2))
            cash_eur_in_usd = int(cash_eur) * eur_to_usd
            cash_eur_in_usd = float(round(cash_eur_in_usd, 2))
            cash_usd = str(round(cash_usd, 2))
            money = cash_uah_in_usd + cash_eur_in_usd + float(cash_usd)
        else:
            usd_to_eur = exchange_rate["usd_to_eur"]
            uah_to_eur = exchange_rate["uah_to_eur"]
            cash_usd_in_eur = int(cash_usd) * usd_to_eur
            cash_usd_in_eur = float(round(cash_usd_in_eur, 2))
            cash_uah_in_eur = int(cash_uah) * uah_to_eur
            cash_uah_in_eur = float(round(cash_uah_in_eur, 2))
            cash_eur = float(round(cash_eur, 2))
            money = cash_usd_in_eur + cash_uah_in_eur + float(cash_eur)
        my_coin = db.execute("SELECT id,count,currency,category,strftime('%d.%m.%Y',daytime) FROM cashflow WHERE cashflow_id = ?", session["user_id"])
        name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        if not my_coin:
            render_template("emptywallet.html",name = name[0]["username"])
        try:
            return render_template("wallet.html", my_coin = my_coin,name = name[0]["username"],money = money,cash_uah = cash_uah,cash_usd = cash_usd,cash_eur =cash_eur,uah_income = uah_income,usd_income = usd_income,eur_income= eur_income,uah_expence =uah_expence,usd_expence = usd_expence, eur_expence = eur_expence)
        except TypeError:
            return render_template("emptywallet.html",name = name[0]["username"])
    else:
        uah_income = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'income' and cashflow_id = ? and currency = 'uah'", session["user_id"])[0]["sum(count)"]
        usd_income = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'income' and cashflow_id = ? and currency = 'usd'", session["user_id"])[0]["sum(count)"]
        eur_income = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'income' and cashflow_id = ? and currency = 'eur'", session["user_id"])[0]["sum(count)"]
        uah_expence = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'expense' and cashflow_id = ? and currency = 'uah'", session["user_id"])[0]["sum(count)"]
        usd_expence = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'expense' and cashflow_id = ? and currency = 'usd'", session["user_id"])[0]["sum(count)"]
        eur_expence = db.execute("SELECT sum(count) FROM cashflow WHERE type = 'expense' and cashflow_id = ? and currency = 'eur'", session["user_id"])[0]["sum(count)"]
        if uah_income is None:
            uah_income = 0
        if usd_income is None:
            usd_income = 0
        if eur_income is None:
            eur_income = 0
        if uah_expence is None:
            uah_expence = 0
        if usd_expence is None:
            usd_expence = 0
        if eur_expence is None:
            eur_expence = 0
        cash_uah = uah_income - uah_expence
        cash_usd = usd_income - usd_expence
        cash_eur = eur_income - eur_expence
        usd_to_uah = exchange_rate["usd_to_uah"]
        eur_to_uah = exchange_rate["eur_to_uah"]
        cash_usd_in_uah = int(cash_usd) * usd_to_uah
        cash_usd_in_uah = float(round(cash_usd_in_uah, 2))
        cash_eur_in_uah = int(cash_eur) * eur_to_uah
        cash_eur_in_uah = float(round(cash_eur_in_uah, 2))
        cash_uah = float(round(cash_uah, 2))
        money = cash_usd_in_uah + cash_eur_in_uah + float(cash_uah)
        my_coin = db.execute("SELECT id,type,count,currency,category,strftime('%d.%m.%Y',daytime) FROM cashflow WHERE cashflow_id = ?", session["user_id"])
        name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        if not my_coin:
            return render_template("emptywallet.html",name = name[0]["username"])
        try:
            return render_template("wallet.html", my_coin = my_coin,name = name[0]["username"],money = money,)
        except TypeError:
            return render_template("emptywallet.html",name = name[0]["username"])


@app.route('/delete-post/<int:deleted_id>')
def delete(deleted_id):
    db.execute("DELETE FROM cashflow WHERE id = ?", int(deleted_id))
    db.execute("DELETE FROM count_cashflow WHERE id = ?", int(deleted_id))
    return redirect("/wallet")


@app.route("/statistics")
@login_required
def statistics():
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    sum_expense_categories = db.execute("SELECT sum(count_entertainment),sum(count_grocery),sum(count_health),sum(count_transport),sum(count_cafe),sum(count_householding),sum(count_others) FROM count_cashflow WHERE count_cashflow_id = ?", session["user_id"])
    sum_income_categories = db.execute("SELECT sum(count_salary),sum(count_other) FROM count_cashflow WHERE count_cashflow_id = ?", session["user_id"])
    salary = sum_income_categories[0]["sum(count_salary)"]
    other = sum_income_categories[0]["sum(count_other)"]
    sum_income = salary + other
    salary = salary/sum_income * 100
    other = other/sum_income * 100
    entertainment = sum_expense_categories[0]["sum(count_entertainment)"]
    grocery = sum_expense_categories[0]["sum(count_grocery)"]
    health = sum_expense_categories[0]["sum(count_health)"]
    transport = sum_expense_categories[0]["sum(count_transport)"]
    cafe = sum_expense_categories[0]["sum(count_cafe)"]
    householding = sum_expense_categories[0]["sum(count_householding)"]
    others = sum_expense_categories[0]["sum(count_others)"]
    sum_expense = entertainment + grocery + health + transport + cafe + householding + others
    entertainment = entertainment/sum_expense * 100
    grocery = grocery/sum_expense * 100
    health = health/sum_expense * 100
    transport = transport/sum_expense * 100
    cafe = cafe/sum_expense * 100
    householding = householding/sum_expense * 100
    others = others/sum_expense * 100
    return render_template("statistics.html",name = name[0]["username"],salary= round(salary,2),other = round(other,2),others= round(others,2),householding=round(householding,2),cafe=round(cafe,2),transport=round(transport,2),health=round(health,2),grocery=round(grocery,2),entertainment=round(entertainment,2))
  

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
        
        if request.form.get("remember") != 'me':
            session.clear()
            app.config["SESSION_PERMANENT"] = False

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        session.clear()
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/home")
@login_required
def home():
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    return render_template("home.html",name = name[0]["username"])


@app.route("/")
def index():
    try:
        name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        return render_template("index.html",name = name[0]["username"])
    except KeyError:
        return render_template("index.html")
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


@app.route("/cashflow", methods=["GET", "POST"])
@login_required
def cashflow():
    if request.method == "POST":
        if not request.form.get("income_count") or not request.form.get("currency_income") or not request.form.get("category_income"):
            if not request.form.get("expense_count") or not request.form.get("currency_expense") or not request.form.get("category_expense"):
                return apology("please correctly enter the expence or income form",400)
            else:
                db.execute("INSERT INTO cashflow(cashflow_id,type,count,currency,category)VALUES(?,'expense',?,?,?)", session["user_id"], int(request.form.get("expense_count")), request.form.get("currency_expense"), request.form.get("category_expense"))
                if request.form.get("currency_expense") == 'uah':
                    uah_to_usd = exchange_rate["uah_to_usd"]
                    count_uah_to_usd = int(request.form.get("expense_count")) * uah_to_usd
                    count_uah_to_usd = str(round(count_uah_to_usd, 2))
                    if request.form.get("category_expense") == 'entertainment':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id,category_cashflow, count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0',?,'0','0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_uah_to_usd)
                    elif request.form.get("category_expense") == 'grocery':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0',?,'0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_uah_to_usd)
                    elif request.form.get("category_expense") == 'health':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0',?,'0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_uah_to_usd)
                    elif request.form.get("category_expense") == 'transport':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0',?,'0','0','0')", session["user_id"],request.form.get("category_expense"), count_uah_to_usd)
                    elif request.form.get("category_expense") == 'cafe':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0',?,'0','0')", session["user_id"],request.form.get("category_expense"), count_uah_to_usd)
                    elif request.form.get("category_expense") == 'householding':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0',?,'0')", session["user_id"], request.form.get("category_expense"),count_uah_to_usd)
                    else:
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0','0',?)", session["user_id"],request.form.get("category_expense"), count_uah_to_usd)
       
                elif request.form.get("currency_expense") == 'eur':
                    eur_to_usd = exchange_rate["eur_to_usd"]
                    count_eur_to_usd = int(request.form.get("expense_count")) * eur_to_usd
                    count_eur_to_usd = str(round(count_eur_to_usd, 2))
                    if request.form.get("category_expense") == 'entertainment':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id,category_cashflow, count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0',?,'0','0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_eur_to_usd)
                    elif request.form.get("category_expense") == 'grocery':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0',?,'0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_eur_to_usd)
                    elif request.form.get("category_expense") == 'health':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0',?,'0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_eur_to_usd)
                    elif request.form.get("category_expense") == 'transport':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0',?,'0','0','0')", session["user_id"],request.form.get("category_expense"), count_eur_to_usd)
                    elif request.form.get("category_expense") == 'cafe':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0',?,'0','0')", session["user_id"],request.form.get("category_expense"), count_eur_to_usd)
                    elif request.form.get("category_expense") == 'householding':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0',?,'0')", session["user_id"], request.form.get("category_expense"),count_eur_to_usd)
                    else:
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0','0',?)", session["user_id"],request.form.get("category_expense"), count_eur_to_usd)
       
                else:
                    if request.form.get("category_expense") == 'entertainment':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id,category_cashflow, count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0',?,'0','0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),int(request.form.get("expense_count")))
                    elif request.form.get("category_expense") == 'grocery':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0',?,'0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),int(request.form.get("expense_count")))
                    elif request.form.get("category_expense") == 'health':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0',?,'0','0','0','0')", session["user_id"], request.form.get("category_expense"),int(request.form.get("expense_count")))
                    elif request.form.get("category_expense") == 'transport':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0',?,'0','0','0')", session["user_id"],request.form.get("category_expense"), int(request.form.get("expense_count")))
                    elif request.form.get("category_expense") == 'cafe':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0',?,'0','0')", session["user_id"],request.form.get("category_expense"), int(request.form.get("expense_count")))
                    elif request.form.get("category_expense") == 'householding':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0',?,'0')", session["user_id"], request.form.get("category_expense"),int(request.form.get("expense_count")))
                    else:
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0','0',?)", session["user_id"],request.form.get("category_expense"), int(request.form.get("expense_count")))
        else:   
            db.execute("INSERT INTO cashflow(cashflow_id,type,count,currency,category)VALUES(?,'income',?,?,?)", session["user_id"], int(request.form.get("income_count")), request.form.get("currency_income"), request.form.get("category_income"))
            if request.form.get("currency_income") == 'uah':
                uah_to_usd = exchange_rate["uah_to_usd"]
                count_uah_to_usd = int(request.form.get("income_count")) * uah_to_usd
                count_uah_to_usd = str(round(count_uah_to_usd, 2))
                if request.form.get("category_income") == 'salary':
                    db.execute("INSERT INTO count_cashflow(count_cashflow_id,category_cashflow, count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,'salary',?,'0','0','0','0','0','0','0','0')", session["user_id"],count_uah_to_usd)
                else:
                    db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,'other','0',?,'0','0','0','0','0','0','0')", session["user_id"],count_uah_to_usd)
               
            elif request.form.get("currency_income") == 'eur':
                eur_to_usd = exchange_rate["eur_to_usd"]
                count_eur_to_usd = int(request.form.get("income_count")) * eur_to_usd
                count_eur_to_usd = str(round(count_eur_to_usd, 2))
                if request.form.get("category_income") == 'salary':
                    db.execute("INSERT INTO count_cashflow(count_cashflow_id,category_cashflow, count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,'salary',?,'0','0','0','0','0','0','0','0')", session["user_id"],count_eur_to_usd)
                else:
                    db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,'other','0',?,'0','0','0','0','0','0','0')", session["user_id"],count_eur_to_usd)
               
            else:
                if request.form.get("category_income") == 'salary':
                    db.execute("INSERT INTO count_cashflow(count_cashflow_id,category_cashflow, count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,'salary',?,'0','0','0','0','0','0','0','0')", session["user_id"], int(request.form.get("income_count")))
                else:
                    db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,'other','0',?,'0','0','0','0','0','0','0')", session["user_id"], int(request.form.get("income_count")))
                    
            if request.form.get("expense_count") and request.form.get("currency_expense") and request.form.get("category_expense"):
                db.execute("INSERT INTO cashflow(cashflow_id,type,count,currency,category)VALUES(?,'expense',?,?,?)", session["user_id"], int(request.form.get("expense_count")), request.form.get("currency_expense"), request.form.get("category_expense"))
                if request.form.get("currency_expense") == 'uah':
                    uah_to_usd = exchange_rate["uah_to_usd"]
                    count_uah_to_usd = int(request.form.get("expense_count")) * uah_to_usd
                    count_uah_to_usd = str(round(count_uah_to_usd, 2))
                    if request.form.get("category_expense") == 'entertainment':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id,category_cashflow, count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0',?,'0','0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_uah_to_usd)
                    elif request.form.get("category_expense") == 'grocery':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0',?,'0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_uah_to_usd)
                    elif request.form.get("category_expense") == 'health':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0',?,'0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_uah_to_usd)
                    elif request.form.get("category_expense") == 'transport':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0',?,'0','0','0')", session["user_id"],request.form.get("category_expense"), count_uah_to_usd)
                    elif request.form.get("category_expense") == 'cafe':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0',?,'0','0')", session["user_id"],request.form.get("category_expense"), count_uah_to_usd)
                    elif request.form.get("category_expense") == 'householding':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0',?,'0')", session["user_id"], request.form.get("category_expense"),count_uah_to_usd)
                    else:
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0','0',?)", session["user_id"],request.form.get("category_expense"), count_uah_to_usd)
       
                elif request.form.get("currency_expense") == 'eur':
                    eur_to_usd = exchange_rate["eur_to_usd"]
                    count_eur_to_usd = int(request.form.get("expense_count")) * eur_to_usd
                    count_eur_to_usd = str(round(count_eur_to_usd, 2))
                    if request.form.get("category_expense") == 'entertainment':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id,category_cashflow, count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0',?,'0','0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_eur_to_usd)
                    elif request.form.get("category_expense") == 'grocery':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0',?,'0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_eur_to_usd)
                    elif request.form.get("category_expense") == 'health':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0',?,'0','0','0','0')", session["user_id"], request.form.get("category_expense"),count_eur_to_usd)
                    elif request.form.get("category_expense") == 'transport':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0',?,'0','0','0')", session["user_id"],request.form.get("category_expense"), count_eur_to_usd)
                    elif request.form.get("category_expense") == 'cafe':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0',?,'0','0')", session["user_id"],request.form.get("category_expense"), count_eur_to_usd)
                    elif request.form.get("category_expense") == 'householding':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0',?,'0')", session["user_id"], request.form.get("category_expense"),count_eur_to_usd)
                    else:
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0','0',?)", session["user_id"],request.form.get("category_expense"), count_eur_to_usd)
       
                else:
                    if request.form.get("category_expense") == 'entertainment':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id,category_cashflow, count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0',?,'0','0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),int(request.form.get("expense_count")))
                    elif request.form.get("category_expense") == 'grocery':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0',?,'0','0','0','0','0')", session["user_id"], request.form.get("category_expense"),int(request.form.get("expense_count")))
                    elif request.form.get("category_expense") == 'health':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0',?,'0','0','0','0')", session["user_id"], request.form.get("category_expense"),int(request.form.get("expense_count")))
                    elif request.form.get("category_expense") == 'transport':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0',?,'0','0','0')", session["user_id"],request.form.get("category_expense"), int(request.form.get("expense_count")))
                    elif request.form.get("category_expense") == 'cafe':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0',?,'0','0')", session["user_id"],request.form.get("category_expense"), int(request.form.get("expense_count")))
                    elif request.form.get("category_expense") == 'householding':
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0',?,'0')", session["user_id"], request.form.get("category_expense"),int(request.form.get("expense_count")))
                    else:
                        db.execute("INSERT INTO count_cashflow(count_cashflow_id, category_cashflow,count_salary,count_other,count_entertainment,count_grocery,count_health, count_transport,count_cafe, count_householding,  count_others )VALUES(?,?,'0','0','0','0','0','0','0','0',?)", session["user_id"],request.form.get("category_expense"), int(request.form.get("expense_count")))
        name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        return render_template("cashflow.html",name = name[0]["username"])
    else:
        name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        return render_template("cashflow.html",name = name[0]["username"])


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
            if request.form.get("newpassword") != request.form.get("confirm") or not request.form.get("confirm") or not request.form.get("newpassword"):
                return apology("your new passwords is different", 400)
            else:
                db.execute("UPDATE users SET hash = ? WHERE id = ?",generate_password_hash(request.form.get("newpassword"), method='pbkdf2:sha256', salt_length=8), session["user_id"])
        return redirect("/login")
    else:
        name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        return render_template("settings.html",name = name[0]["username"])


if __name__ == '__main__':
    app.run(debug=True)
