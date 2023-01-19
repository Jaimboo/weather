from ast import Global
from flask import flash, Blueprint, g, redirect, render_template, current_app, request, url_for, session

from werkzeug.exceptions import abort

from weather.auth import login_required
from weather.db import get_db

import json
import requests
import os

from datetime import datetime, timedelta, timezone

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    # Check if the session has already a city value or add a deafult one
    if session.get('city') is None:
        session['city'] = 'Rome'
        session['recent'] = [session['city']]

    # Update json file if needed
    if session.get('new') is not None:
        get_api(session['city'], new = True)
        session.pop('new', default=None)
    else:
        get_api(session['city'])  

    return render_template('index.html')


@bp.route('/days')
def days():
    # Update json file if needed
    get_api(session['city'])
            
    return render_template('days.html')


@bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    data = search_api(q)
    return render_template('results.html', data=data)

@bp.route('/search/<string:city>')
def set_city(city):
    session['city'] = city
    try:
        index = session['recent'].index(city)
        session['recent'].pop(index)
    except ValueError:
        pass
    session['recent'].insert(0, city)
    if len(session['recent']) > 5:
        session['recent'].pop(5)
    session['new'] = True
    return redirect(url_for('api.index'))


# Helpers functions
def get_api(city, new=False):
    # Check if the session has a last updated or if it is older than 15 minutes, than updated the json.
    if session.get('last_u') is None or session.get('last_u') + timedelta(minutes = 60) < datetime.utcnow().replace(tzinfo=timezone.utc) or new == True:
        data = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={current_app.config["SECRET_KEY"]}&q={city}&days=3&aqi=yes&alerts=yes')
        print('updated')
        session['data'] = data.json()
        session['last_u'] =  datetime.utcnow().replace(tzinfo=timezone.utc)

def search_api(q):
    response = requests.get(f'http://api.weatherapi.com/v1/search.json?key={current_app.config["SECRET_KEY"]}&q={q}')
    return response.json()

@bp.route('/favorite')
@login_required
def favorite():
    city = request.args.get('city')
    add = request.args.get('add')
    db = get_db()

    if add == "True":
        db.execute("INSERT INTO favorite (city, u_id) VALUES (?, ?)", (city, session['user_id']))
        db.commit()

        
    elif add == "False":
        db.execute("DELETE FROM favorite WHERE city = ? AND u_id = ?", (city, session['user_id']))
        db.commit()
    
    session['favorite'] = []
    for row in db.cursor().execute('SELECT city FROM favorite WHERE u_id = ?', (session['user_id'],)).fetchall():
        session['favorite'].append(row['city'])

    return redirect(url_for('api.index'))

# jinja template filters
@bp.app_template_filter()
def datetimeformat(value, format='%Y/%m/%d %H-%M'):
    date = datetime.fromtimestamp(value).strftime(format)
    return date

@bp.app_template_filter()
def day(value, format='%d'):
    date = datetime.fromtimestamp(value).strftime(format)
    return date

@bp.app_template_filter()
def day_str(value, format='%a'):
    date = datetime.fromtimestamp(value).strftime(format)
    return date
    
@bp.app_template_filter()
def date(value, format='%d/%m %H:%M'):
    date = datetime.fromtimestamp(value).strftime(format)
    return date

@bp.app_template_filter()
def hour(value, format='%H'):
    date = datetime.fromtimestamp(value).strftime(format)
    return date