#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for

from . import main
from .forms import LoginForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    # send_mail('280108904@qq.com', '欢迎')
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None:
            user = User(username=login_form.username.data, \
                        password=login_form.password.data)
            db.session.add(user)
        session['name'] = login_form.username.data
        return redirect(url_for('.index'))

    return render_template('index.html', form=login_form, name=session.get('name'))