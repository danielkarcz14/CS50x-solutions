import functools 
import re

email_validate_pattern = r"^\S+@\S+\.\S+$"
password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$"

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')



@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        repeated_password = request.form['repeated_password']

        db = get_db()
        error = None
        if not name:
            error = 'Name is required'
        elif not surname:
            error = 'Surname is required'
        elif not email:
            error = 'Email is required'
        if not re.match(email_validate_pattern, email):
            error = 'This is not valid email address!'
        elif not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif not re.match(password_pattern, password):
            error = 'Wrong format! Password must have: at least 8 characters, at least one uppercase and one lowercase letter, at least one digit'
        elif password != repeated_password:
            error = 'Passwords are not matching'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (name, surname, email, username, password) VALUES (?, ?, ?, ?, ?)",
                    (name, surname, email, username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = "Username does not exist!"
        elif not check_password_hash(user['password'], password):
            error = 'Wrong password!'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/login')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

