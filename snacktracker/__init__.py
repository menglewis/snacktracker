# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.migrate import Migrate
from flask.ext.admin import Admin
from settings import ProdConfig

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
admin = Admin()

def create_app(config_object=ProdConfig):

    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    return app

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    admin.init_app(app)

    return None

def register_blueprints(app):
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/accounts')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager.login_view = "auth.login"

    return None

def register_errorhandlers(app):
    def render_error(error):
        return render_template("{0}.html".format(error.code)), error.code
    for errcode in [404, 500]:
        app.errorhandler(errcode)(render_error)
    return None