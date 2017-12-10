#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app, flash, render_template, session, redirect, url_for, abort, request, make_response
from flask_login import current_user, login_required
from . import main
from .forms import LoginForm, EditProfileForm, PostForm, CommentForm
from .. import db
from ..models import User, Post, Comment

@main.route('/', methods=['GET', 'POST'])
def index():
    # send_mail('280108904@qq.com', '欢迎')
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data, body=post_form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed',''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query

    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items

    return render_template('index.html', form=post_form,  posts=posts, show_followed=show_followed, pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)

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
    return render_template('edit-profile.html', form=edit_profile_form)


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        comment = Comment(body=comment_form.body.data, post=post, author=current_user._get_current_object())
        db.session.add(comment)
        flash('已成功发表评论！')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count()-1)/current_app.config['FLASKY_COMMENTS_PER_PAGE']+1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False
    )
    comments = pagination.items
    return render_template('post.html', posts=[post], form=comment_form, comments=comments, pagination=pagination)



@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    post_form = PostForm()
    if post_form.validate_on_submit():
        post.title = post_form.title.data
        post.body = post_form.body.data
        db.session.add(post)
        flash('已成功修改文章！')
        return redirect(url_for('.post', id=post.id))
    post_form.title.data = post.title
    post_form.body.data = post.body
    return render_template('edit_post.html', form = post_form)

@main.route('/editpost', methods=['GET', 'POST'])
@login_required
def editpost():
    post_form = PostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data, body=post_form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        flash('已成功发表博客！')
        post = Post.query.filter_by(author=current_user._get_current_object()).order_by
        return redirect(url_for('.user', username=current_user.username))
    return render_template('edit_post.html', form=post_form)


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
    pagination = user.followed.paginate(
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

@main.route('/moderate')
@login_required
def moderate():
    page = request.args.get('page',1,type=int)
    Comment.query.join(Post, Post.id == Comment.post_id).filter(Post.author_id == 1).all()
    pagination = Comment.query.join(Post,Post.id==Comment.post_id).filter(Post.author_id==current_user.id,Comment.disabled==True).order_by(Comment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'], error_out=False
    )
    comments = pagination.items
    return render_template('moderate.html', comments=comments, pagination=pagination, page=page)

@main.route('/moderate/enable/<int:id>')
@login_required
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    return redirect(url_for('.moderate',page=request.args.get('page',1,type=int)))

@main.route('/moderate/disable/<int:id>')
@login_required
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    return redirect(url_for('.post',id=comment.post_id))