from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from flask.ext.admin import Admin
from utils import make_celery

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

bcrypt = Bcrypt()

admin = Admin(app)

#celery = make_celery(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from app import views, models, admin_instance