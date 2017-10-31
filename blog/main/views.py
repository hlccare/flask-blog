#!/usr/bin/env python
# -*- coding: utf-8 -*-
<<<<<<< HEAD
from flask import current_app, flash, render_template, session, redirect, url_for, abort, request, make_response
=======
from flask import current_app, flash, render_template, session, redirect, url_for, abort, request
>>>>>>> bravo
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
<<<<<<< HEAD
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed',''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
=======
>>>>>>> bravo
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
<<<<<<< HEAD
    return render_template('index.html', form=post_form, posts=posts, pagination=pagination)
=======
    return render_template('index.html', form=post_form,  posts=posts, pagination=pagination)
>>>>>>> bravo


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
<<<<<<< HEAD
    return render_template('user.html', user=user, posts=posts)
=======
    return render_template('user.html', user=user)
>>>>>>> bravo


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

<<<<<<< HEAD

=======
>>>>>>> bravo
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
<<<<<<< HEAD
    return render_template('edit_post.html', form = post_form)


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('已关注此用户')
        return redirect(url_for('.user',username=username))
    current_user.follow(user)
    flash('成功关注%s' % username)
    return redirect(url_for('.user',username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('尚未关注此用户')
        return redirect(url_for('.user',username=username))
    current_user.unfollow(user)
    flash('成功取消关注%s' % username)
    return redirect(url_for('.user',username=username))

@main.route('/follows/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    follows = [{'user':item.follower, 'timestamp':item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination, follows=follows)

@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    follows = [{'user':item.followed, 'timestamp':item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination, follows=follows)

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','', max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp
=======
    return render_template('edit_post.html', form = post_form)
>>>>>>> bravo
