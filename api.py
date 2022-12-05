from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

from weather.auth import login_required
from weather.db import get_db

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

