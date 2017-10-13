#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import mail
from flask import current_app
from flask_mail import Message
from threading import Thread

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, **kwargs):
    blog = current_app._get_current_object()
    msg = Message(subject=blog.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=blog.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    # body/html 可渲染模版 page 61
    msg.body = 'testingbody'
    msg.html = 'testinghtml'
    thr = Thread(target=send_async_email, args=[blog, msg])
    thr.start()
    return thr