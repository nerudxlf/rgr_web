from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from configparser import SafeConfigParser

config = SafeConfigParser()
config.read('config.ini')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.get("FILES", "DATABASE")
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpeg', 'jpg'])
app.secret_key = config.get("DEFAULT", "SECRET_KEY")
db = SQLAlchemy(app)
manager = LoginManager(app)

from main import routs, db_worker

db.create_all()
