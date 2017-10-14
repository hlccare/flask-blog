#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))

    def __repr__(self):
        return '<User %r>' % self.username



