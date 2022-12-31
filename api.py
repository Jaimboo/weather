from flask import Blueprint, flash, g, jsonify, redirect, render_template, current_app, request, url_for, session

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
    if session.get('city') is None:
        session['city'] = 'Rome'

    get_api(session['city'])

    with open(os.path.join(current_app.instance_path, 'api_response.json'), 'r') as f:
        data = json.load(f)
        d = {
            'location': data['location'],
            'current': data['current'],
            'alerts': data['alerts']
        }
    return render_template('index.html', data=d)

@bp.route('/days')
def days():
    with open(os.path.join(current_app.instance_path, 'api_response.json'), 'r') as f:
        data = json.load(f)

        d = {
            'location': data['location'],
            'forecast': []
        }
        for x in data['forecast']['forecastday']:
            y = {key:x[key] for key in ['date_epoch', 'day', 'hour']}
            d['forecast'].append(y)
            
    return render_template('days.html', data=d)


@bp.route('/search', methods=['GET'])
def search():
    q = request.args.get('q')
    data = search_api(q)
    return render_template('results.html', data=data)

@bp.route('/search/<string:city>')
def set_city(city):
    session['city'] = city
    return redirect(url_for('api.index'))

def get_api(city):
    if os.path.exists(os.path.join(current_app.instance_path, 'api_response.json')) == False:
        session.clear()
    if session.get('last_u') is None or session['last_u'] + timedelta(minutes = 15) < datetime.utcnow().replace(tzinfo=timezone.utc):
        print('updated')
        data = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={current_app.config["SECRET_KEY"]}&q={city}&days=3&aqi=no&alerts=yes')
        session['last_u'] = datetime.utcnow()
        with open(os.path.join(current_app.instance_path, 'api_response.json'), 'w') as f:
            f.truncate()
            json.dump(data.json(), f)

def search_api(q):
    response = requests.get(f'http://api.weatherapi.com/v1/search.json?key={current_app.config["SECRET_KEY"]}&q={q}')
    return response.json()

@bp.app_template_filter()
def datetimeformat(value, format='%Y/%m/%d %H:%M'):
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
def hour(value, format='%H'):
    date = datetime.fromtimestamp(value).strftime(format)
    return date