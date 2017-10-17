#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import flash, render_template, session, redirect, url_for, abort
from flask_login import current_user, login_required
from . import main
from .forms import LoginForm, EditProfileForm, PostForm
from .. import db
from ..models import User, Post

@main.route('/', methods=['GET', 'POST'])
def index():
    # send_mail('280108904@qq.com', '欢迎')
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(body=post_form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    return render_template('index.html', form=post_form)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edit_profile_form = EditProfileForm()
    if edit_profile_form.validate_on_submit():
        current_user.name = edit_profile_form.name.data
        current_user.location = edit_profile_form.location.data
        current_user.connect_mail = edit_profile_form.connect_mail.data
        current_user.about_me = edit_profile_form.about_me.data
        db.session.add(current_user)
        flash('已成功修改个人资料！')
        return redirect(url_for('.user', username=current_user.username))
    edit_profile_form.name.data = current_user.name
    edit_profile_form.location.data = current_user.location
    edit_profile_form.connect_mail.data = current_user.connect_mail
    edit_profile_form.about_me.data = current_user.about_me
    return render_template('main/edit-profile.html', form=edit_profile_form)