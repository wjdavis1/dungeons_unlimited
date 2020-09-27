from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_required
from app import db
from app.main import bp

@bp.route('/')
@bp.route('/index')
def index():
    return 'Hello, World!'
