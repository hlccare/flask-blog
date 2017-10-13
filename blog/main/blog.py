#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, session, url_for, redirect, request
from flask_script import Manager
from flask_bootstrap import Bootstrap
from forms import RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_script import Shell
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message
from threading import Thread
import sys

reload(sys)
sys.setdefaultencoding('utf8')

basedir = os.path.abspath(os.path.dirname(__file__))

blog = Flask(__name__)
blog.config['SECRET_KEY'] = 'secret_key'
blog.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
blog.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
blog.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
blog.config['MAIL_SERVER'] = 'smtp.qq.com'
blog.config['MAIL_PORT'] = 465
blog.config['MAIL_USE_SSL'] = True
blog.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or '280108904'
blog.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'aujdblcogbembjje'
blog.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[认证]'
blog.config['FLASKY_MAIL_SENDER'] = '博客认证<280108904@qq.com>'
manager = Manager(blog)
bootstrap = Bootstrap(blog)
db = SQLAlchemy(blog)
mail = Mail(blog)
migrate = Migrate(blog, db)
manager.add_command('db', MigrateCommand)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' % self.username


@blog.route('/', methods=['GET', 'POST'])
def index():
    send_mail('280108904@qq.com', '欢迎')
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None:
            user = User(username=login_form.username.data, \
                        password=login_form.password.data)
            db.session.add(user)
        session['name'] = login_form.username.data
        return redirect(url_for('index'))

    return render_template('index.html', form=login_form, name=session.get('name'))





def make_shell_context():
    return dict(blog=blog, db=db, User=User)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    # blog.run(debug=True)
    manager.run()
