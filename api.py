from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

from weather.auth import login_required
from weather.db import get_db

import json
from datetime import datetime

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    with open('weather/placeholder.json', 'r') as f:
        data = json.load(f)
    return render_template('index.html', data=data)

@bp.route('/days')
def days():
    with open('weather/placeholder.json', 'r') as f:
        data = json.load(f)

        d = {
            'location': data['location'],
            'forecast': []
        }
        for x in data['forecast']['forecastday']:
            y = {key:x[key] for key in ['date_epoch', 'day', 'hour']}
            d['forecast'].append(y)
            
    return render_template('days.html', data=d)

@bp.route('/days/<int:id>/')
def hourly(id):
    with open('weather/placeholder.json', 'r') as f:
        data = json.load(f)
        d = {
            key:data[key] for key in [data['location'], data['forecast']['forecastday'][id]]
        }

    return render_template('hourly.html', data=d)

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