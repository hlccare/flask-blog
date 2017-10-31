#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import current_app, flash, render_template, session, redirect, url_for, abort, request
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
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    return render_template('index.html', form=post_form,  posts=posts, pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
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

@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html',posts=[post])



@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    post_form = PostForm()
    if post_form.validate_on_submit():
        post.body = post_form.body.data
        db.session.add(post)
        flash('已成功修改文章！')
        return redirect(url_for('.post', id=post.id))
    post_form.body.data = post.body
    return render_template('edit_post.html', form = post_form)