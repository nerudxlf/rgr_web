from flask import render_template, request, flash, url_for, redirect, g
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from main import db, app
from .db_worker import *


@app.route('/')
def index():
    return render_template('index.html', title_name="Знакомства.ru")


@app.route('/home')
def home():
    return render_template('home.html', title_name="Home")


@app.route('/message')
def message():
    return render_template('message.html', title_name="Message")


@app.route('/settings')
def setings():
    return render_template('settings.html', title_name="Settings")
