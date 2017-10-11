from flask import Flask, render_template, session, url_for, redirect, request
from flask_script import Manager
from flask_bootstrap import Bootstrap
from forms import RegisterForm

import sys
reload(sys)
sys.setdefaultencoding('utf8')

blog = Flask(__name__)
blog.config['SECRET_KEY'] = 'secret_key'
manager = Manager(blog)
bootstrap = Bootstrap(blog)


@blog.route('/', methods=['GET', 'POST'])
def index():
    register_form = RegisterForm()
    return render_template('index.html', form=register_form)


if __name__ == '__main__':
    # blog.run(debug=True)
    manager.run()
