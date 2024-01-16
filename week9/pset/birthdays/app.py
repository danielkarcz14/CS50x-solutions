import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

# get atributes
def get_id():
    return request.form.get("id")
def get_name():
    return request.form.get('name')
def get_month():
    return request.form.get('month')
def get_day():
    return request.form.get('day')
def get_birthdays():
    return db.execute("SELECT * FROM birthdays")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get('name')
        month = request.form.get('month')
        day = request.form.get('day')

        if not name or not month or not day:
            return redirect("/")
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)
        birthdays = get_birthdays()
        return render_template("index.html", birthdays=birthdays)

    else:

        # TODO: Display the entries in the database on index.html
        birthdays = get_birthdays()
        return render_template("index.html", birthdays=birthdays)


# my own additions of delete and edit

@app.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        id = get_id()
        db.execute("DELETE FROM birthdays WHERE id = ?", id)
        birthdays = get_birthdays()
        return render_template("index.html", birthdays=birthdays)


@app.route("/edit", methods=["POST"])
def edit():
    if request.method == "POST":
        id = get_id()
        name = db.execute("SELECT name FROM birthdays WHERE id = ?", id)[0]['name']
        month = db.execute("SELECT month FROM birthdays WHERE id = ?", id)[0]['month']
        day = db.execute("SELECT day FROM birthdays WHERE id = ?", id)[0]['day']
        return render_template("edit.html", id=id, name=name, month=month, day=day)


@app.route("/edited", methods=["POST"])
def edited():
    if request.method == "POST":
        id = get_id()
        name = get_name()
        month = get_month()
        day = get_day()
        if not name or not month or not day:
            return redirect("/")
        db.execute("UPDATE birthdays SET name = ?, month = ?, day = ? WHERE id = ?", name, month, day, id)
        birthdays = get_birthdays()
        return render_template("index.html", birthdays=birthdays)




