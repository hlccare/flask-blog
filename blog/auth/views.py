#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegisterForm, ChangePasswordForm, ChangeUsernameForm
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
@login_required
def change_password():
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        if current_user.verify_password(change_password_form.old_password.data):
            current_user.password = change_password_form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            flash('已成功修改密码！')
            logout()
            return redirect(url_for('main.index'))
        else:
            flash('原密码不正确！')
    return render_template('auth/change_password.html',form=change_password_form)

@auth.route('/change-username', methods=['GET', 'POST'])
@login_required
def change_username():
    change_username_form = ChangeUsernameForm()
    if change_username_form.validate_on_submit():
        current_user.username = change_username_form.new_username.data
        db.session.add(current_user)
        db.session.commit()
        flash('已成功修改用户名！')
        return redirect(url_for('main.index'))
    return render_template('auth/change_username.html', form=change_username_form)
