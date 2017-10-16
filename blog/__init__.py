#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'



def create_app(config_name):
    blog = Flask(__name__)
    blog.config.from_object(config[config_name])
    config[config_name].init_app(blog)

    bootstrap.init_app(blog)
    mail.init_app(blog)
    db.init_app(blog)
    login_manager.init_app(blog)

    with blog.app_context():
        db.create_all()

    from .main import main as main_blueprint
    blog.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    blog.register_blueprint(auth_blueprint, url_prefix='/auth')

    return blog
