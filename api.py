from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

from weather.auth import login_required
from weather.db import get_db

import json

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    with open('weather/placeholder.json', 'r') as f:
        data = json.load(f)
    return render_template('index.html', data=data)

