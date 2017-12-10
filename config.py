#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[认证]'
    FLASKY_MAIL_SENDER = '博客认证<280108904@qq.com>'
    FLASKY_POSTS_PER_PAGE = 15
    FLASKY_FOLLOWERS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 5
    SSL_DISABLE = 1


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_USER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '280108904'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'aujdblcogbembjje'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                 'dev-test.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,
                                                                                                 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://suaivpipztvobe:684afa330e01d21059c447babb9eaff898d78492f2bf1c3d3112ba646e5d8645@ec2-184-72-243-166.compute-1.amazonaws.com:5432/dfi324i5tsleji'

class HerokuConfig(Config):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def __init__(app):
        ProductionConfig.init_app(app)
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}
