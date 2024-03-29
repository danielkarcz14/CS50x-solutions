# I will also upload version with SQLAlchemy

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

from datetime import datetime

# Configure application
app = Flask(__name__)


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    # get attributes\
    shares = db.execute("SELECT symbol, quantity, share_price, total_price FROM portfolio WHERE user_id = ?", session["user_id"])
    balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']
    total_stock = db.execute("SELECT SUM(total_price) FROM portfolio WHERE user_id = ?", session["user_id"])[0]["SUM(total_price)"]
    if total_stock is None:
        total_stock = 0
    total_value = balance + total_stock
    return render_template("index.html", shares=shares, balance=round(balance, 2), total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        quantity = request.form.get("shares")
        try:
            quantity = int(quantity)
        except ValueError:
            return apology("Number of shares must be a positive integer", 400)
        if int(quantity) < 1:
            return apology("Number of shares must be a positive integer", 400)
        if lookup(symbol) is None or not symbol:
            return apology("INVALID SYMBOL", 400)

        # current price
        stock_price = lookup(symbol)['price']
        total_price = float(stock_price) * float(quantity)

        # current users cash
        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']
        new_cash = float(current_cash) - float(total_price)
        # check for enough balance
        if new_cash < 0:
            return apology("Insuficient funds!", 400)

        # update db
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

        # add record to transactions
        time = datetime.now()
        db.execute("INSERT INTO transactions (symbol, quantity, share_price, time, user_id) VALUES(?, ?, ?, ?, ?)",
                   symbol.upper(), quantity, stock_price, time, session["user_id"])

        # add new record to portfolio if one does not exists for the symbol
        if not db.execute("SELECT symbol FROM portfolio WHERE symbol = ? AND user_id = ?", symbol, session["user_id"]):
            db.execute("INSERT INTO portfolio (symbol, quantity, share_price, total_price, time, user_id) VALUES(?, ?, ?, ?, ?, ?)",
                       symbol.upper(), quantity, stock_price, total_price, time, session["user_id"])
            return redirect("/")

        else:
            # or update existing record
            old_quantity = db.execute("SELECT quantity FROM portfolio WHERE user_id = ? AND symbol = ?",
                                      session["user_id"], symbol)[0]["quantity"]
            new_quantity = old_quantity + quantity

            old_total_price = db.execute("SELECT total_price FROM portfolio WHERE user_id = ? AND symbol = ?",
                                         session["user_id"], symbol)[0]["total_price"]
            new_total_price = old_total_price + total_price
            db.execute("UPDATE portfolio SET quantity = ?, share_price = ?, total_price = ? WHERE symbol = ? AND user_id = ?",
                       new_quantity, stock_price, new_total_price, symbol, session["user_id"])
            return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT symbol, quantity, share_price, time FROM transactions WHERE user_id = ?", session["user_id"])
    return render_template("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        # print(f"return of lookup = {lookup(symbol)}")
        if lookup(symbol) is None:
            return apology("INVALID SYMBOL", 400)
        return render_template("quoted.html", symbol=symbol, price=lookup(symbol)['price'])
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        name = request.form.get("username")
        password = request.form.get("password")
        confirmation_password = request.form.get("confirmation")

        if not name or not password or not confirmation_password:
            return apology("invalid username and/or password", 400)
        if password != confirmation_password:
            return apology("Passwords are not matching", 400)
        if db.execute("SELECT username FROM users WHERE username = ?", name):
            return apology("Username already exists", 400)

        result = password_check(password)
        if result is not None:
            return result

        hashed_password = generate_password_hash(password)
        # print(f"{name} {hashed_password}")
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, hashed_password)
        return render_template("login.html")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_symbols = db.execute("SELECT DISTINCT symbol FROM portfolio WHERE user_id = ?", session["user_id"])
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        if not symbol:
            return apology("Select symbol please", 400)

        quantity = request.form.get("shares")
        try:
            quantity = int(quantity)
        except ValueError:
            return apology("Number of shares must be a positive integer", 400)
        if int(quantity) < 1:
            return apology("Number of shares must be a positive integer", 400)

        # check if user has enough shares to sell
        current_quantity = db.execute("""
                                   SELECT SUM(quantity) FROM portfolio
                                   WHERE user_id = ? AND symbol = ?
                                   GROUP BY SYMBOL
                                   """,
                                      session["user_id"], symbol
                                      )[0]['SUM(quantity)']
        current_quantity = int(current_quantity)

        if quantity > current_quantity:
            return apology("You don't have that many shares", 400)

        # update cash
        stock_price = lookup(symbol)['price']
        total_price = stock_price * quantity
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]['cash']
        new_balance = balance + total_price

        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, session["user_id"])

        # update existing record
        new_quantity = current_quantity - quantity
        old_total_price = db.execute("SELECT total_price FROM portfolio WHERE user_id = ? AND symbol = ?",
                                     session["user_id"], symbol)[0]["total_price"]
        new_total_price = old_total_price - total_price
        db.execute("UPDATE portfolio SET quantity = ?, share_price = ?, total_price = ? WHERE symbol = ? AND user_id = ?",
                   new_quantity, stock_price, new_total_price, symbol, session["user_id"])

        # delete from portfolio if quantity is = 0
        if new_quantity == 0:
            db.execute("DELETE FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)

        # add record to transactions
        quantity = quantity * -1
        time = datetime.now()
        db.execute("INSERT INTO transactions (symbol, quantity, share_price, time, user_id) VALUES(?, ?, ?, ?, ?)",
                   symbol.upper(), quantity, stock_price, time, session["user_id"])

        return redirect("/")

    return render_template("sell.html", user_symbols=user_symbols)


def password_check(string):
    if len(string) < 6:
        return apology("At least 6 characters", 400)

    if not any(char.isdigit() for char in string):
        return apology("Must contain atleast one digit", 400)

    if not any(char.isupper() for char in string):
        return apology("Must contain atleast one uppercase letter", 400)

    if not any(char.islower() for char in string):
        return apology("Must contain atleast one lowercase letter", 400)
