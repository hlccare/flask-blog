from flask import Flask, render_template, session, url_for, redirect, request
from flask_script import Manager
from flask_bootstrap import Bootstrap

blog = Flask(__name__)
manager = Manager(blog)
bootstrap = Bootstrap(blog)

@blog.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    #blog.run(debug=True)
    manager.run()
