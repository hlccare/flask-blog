#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_pagedown import PageDown
from config import config
from flask_pagedown import PageDown
from flask_moment import Moment

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
pagedown = PageDown()
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
    moment.init_app(blog)
    login_manager.init_app(blog)
    pagedown.init_app(blog)

    from flask_sslify import SSLify

    sslify = SSLify(blog)

    with blog.app_context():
        db.create_all()

    from .main import main as main_blueprint
    blog.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    blog.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_1_0_blueprint
    blog.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return blog
