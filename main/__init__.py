#!/usr/bin/env python

from datetime import datetime

from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, g
from jinja2 import TemplateNotFound


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
