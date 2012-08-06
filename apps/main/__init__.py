#!/usr/bin/env python

import os.path
from datetime import datetime
from hashlib import md5

from flask import Blueprint, render_template, redirect, request, url_for

from flask.ext.login import login_required

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('blog.entries'))


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/projects')
def projects():
    return render_template('projects.html')

