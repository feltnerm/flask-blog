import re

from datetime import datetime
from unicodedata import normalize

from experientiarum.extensions import db
from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, g
from jinja2 import TemplateNotFound
from werkzeug.security import generate_password_hash, check_password_hash

from forms import UserForm


users = Blueprint('users', __name__, template_folder='templates')

@users.route('/login/', methods = ['GET', 'POST'])
def login():
    
    form = UserForm()
    
    if form.validate_on_submit():
        pass


@users.route('/logout/', methods = ['GET', 'POST'])
def logout():
    pass