import re

from datetime import datetime
from unicodedata import normalize

from experientiarum.extensions import db
from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, g
from jinja2 import TemplateNotFound


users = Blueprint('users', __name__, template_folder='templates')

@users.route('/login/')
def login():
    pass

@users.route('/logout/')
def logout():
    pass