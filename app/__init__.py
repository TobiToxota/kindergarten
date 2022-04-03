from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# initiliaze the flask app
app = Flask(__name__)

# initialze the SECRET_KEY
app.config['SECRET_KEY'] = 'VERY_BAD_SECRET_KEY'

# initiliaze the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/kindergarten.db'
db = SQLAlchemy(app)

from app.models import Kindergarten, Dish, Upload, Parent, Announcement
from app.register import register
from app.login import login
from app.home import home, index
from app.announcements import addAnouncement
