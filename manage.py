#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from blog import create_app, db
from blog.models import User, Post, Follow, Comment
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

reload(sys)
sys.setdefaultencoding('utf8')
blog = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(blog)
migrate = Migrate(blog, db)


@manager.command
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


def make_shell_context():
    return dict(blog=blog, db=db, User=User, Post=Post, Follow=Follow, Comment=Comment)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
