import re

from datetime import datetime
from unicodedata import normalize

from experientiarum.extensions import db
from experientiarum.helpers import slugify
from forms import EntryForm
from flask import Blueprint, render_template, abort, request, redirect, \
    url_for, current_app, flash, g
from jinja2 import TemplateNotFound


admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/login')
def login():
    pass

@admin.route('/logout')
def logout():
    pass