#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from forms import RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()


def create_app(config_name):
    blog = Flask(__name__)
    blog.config.from_object(config[config_name])
    config[config_name].init_app(blog)

    bootstrap.init_app(blog)
    mail.init_app(blog)
    db.init_app(blog)

    return blog
