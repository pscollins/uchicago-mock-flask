import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = "{}/data".format(BASE_DIR)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/data.db'.format(DATA_DIR)
db = SQLAlchemy(app)

from mockchicago import views
