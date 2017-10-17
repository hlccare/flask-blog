#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_Form = LoginForm()
    if login_Form.validate_on_submit():
        user = User.query.filter_by(email=login_Form.email.data).first()
        if user is not None and user.verify_password(login_Form.password.data):
            login_user(user, login_Form.remember_me.data)
            return redirect(url_for('main.index'))
        else:
            flash('帐号或者密码错误！请重新输入')
    return render_template('auth/login.html', form=login_Form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已成功退出！')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    register_Form = RegisterForm()
    if register_Form.validate_on_submit():
        user = User(email=register_Form.email.data,
                    username=register_Form.username.data,
                    password=register_Form.password.data)
        db.session.add(user)
        flash('已成功注册')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=register_Form)

@auth.route('/change-password', methods=['GET', 'POST'])
def change_password():
    pass

@auth.route('/change-username', methods=['GET', 'POST'])
def change_username():
    pass