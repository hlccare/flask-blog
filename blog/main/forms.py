#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email
from flask_pagedown.fields import PageDownField


class PostForm(FlaskForm):
    body = PageDownField('写下你的想法', validators=[DataRequired()])
    submit = SubmitField('提交')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('请再次输入密码',
                              validators=[DataRequired, EqualTo('password', message='密码不一致，请重新输入')])
    submit = SubmitField('注册')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


class EditProfileForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])
    location = StringField('所在地', validators=[DataRequired()])
    connect_mail = StringField('联系邮箱', validators=[DataRequired(), Email()])
    about_me = TextAreaField('简单描述', validators=[DataRequired()])
    summit = SubmitField('提交修改')