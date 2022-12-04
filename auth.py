import functools

from flask import abort, Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash

from weather.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        
        if not username:
            abort(400, 'Username is required')
        if not password:
            abort(400, 'Password is required')

        try:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)', (username, generate_password_hash(password)) )
            db.commit()
        except db.IntegrityError:
            abort(400, 'User already registered')
        
    return render_template('register.html')