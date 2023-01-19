import functools
from sqlite3 import OperationalError

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from weather.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # Getting username and password
        username = request.form['username']
        password = request.form['password']

        # searching for a database
        db = get_db()

        error = None

        # checking for errors
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:
                # insert username and passord into the database if no error occur
                db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password)) )
                db.commit()
            except db.IntegrityError:
                error = 'User already registered'
            else:
                # redirect to login view if no error occur
                flash('Succefully registered. Now you can login.', 'success')
                return redirect(url_for('auth.login'))

        flash(error, 'warning')

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # getting username and password
        username = request.form['username']
        password = request.form['password']
        
        # checking for database
        db = get_db()

        error = None

        # checking for error
        if not username:
            error = 'Username is required.'
        if not password:
            error = 'Password is required'
        
        user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        if user is None or not check_password_hash(user['password'], password):
            error = 'Incorrect credentials.'

        if error is None:
            # clearing session and creatinga new one with the requested user
            session.clear()
            session['user_id'] = user['id']
            session['favorite'] = []
            for row in db.cursor().execute('SELECT city FROM favorite WHERE u_id = ?', (session['user_id'],)).fetchall():
                session['favorite'].append(row['city'])
            flash(f'Welcome,{username}', 'success')
            return redirect(url_for('api.index'))

        flash(error, 'danger')

    return render_template('/login.html')

@bp.before_app_request
def load_logged_in_user():
    try:
        if session.get('user_id') is None:
            g.user = None
        else:
            g.user = get_db().execute('SELECT username, id FROM user WHERE id = ? ', (session.get('user_id'), )).fetchone()
    except OperationalError:
        session.clear()    

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('api.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view