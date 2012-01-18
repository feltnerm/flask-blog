#!/usr/bin/env python

'''
    experientiarum
    
    ~ a place where I can leave my experiences
'''

__author__ = "Mark Feltner"
__copyright__ = "Copyright 2012, Mark Feltner"
__credits__ = ["Mark Feltner"]
__license__ = ""
__version__ = ""
__maintainer__ = "Mark Feltner"
__email__ = "feltner.mj@gmail.com"
__status__ = "Development"

import os

import logging
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

from flask import Flask, g, request, flash, redirect, url_for, Markup,\
    render_template
    
from flaskext.assets import Environment
from flaskext.principal import Principal

from experientiarum import helpers
from experientiarum.extensions import db


def configure_before_handlers(app):
    ''' @todo: wtf is this? '''
    
    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)

def configure_blueprints(app):
    ''' Register blueprints. '''
    
    # Main
    from main import main
    app.register_blueprint(main)
    
    # Users
    from users import users
    app.register_blueprint(users)
    
    from users.models import User
    db.register([User])
        
    # BLOG
    from blog import blog
    app.register_blueprint(blog, url_prefix = '/blog')

    from blog.models import Entry
    db.register([Entry])
    
    '''
    # BOOKMARKS
    from bookmarks import bookmarks
    app.register_blueprint(bookmarks, url_prefix = '/bookmarks')
    
    # PASTEBIN
    from pastebin import pastebin
    app.register_blueprint(pastebin, url_prefix = '/pastebin')
    
    # READLATERS
    from readlaters import readlaters
    app.register_blueprint(readlaters, url_prefix = '/readlaters')
    
    # TODO
    from todo import todo
    app.register_blueprint(todo, url_prefix = '/todo')
    '''

def configure_errorhandlers(app):
    ''' Set up default HTTP error pages '''

    @app.error_handler(401)
    def unauthorized(error):
        if request.is_xhr:
            return jsonify(error="Login required.")
        flash("Please login to see this page.", "error")
        return render_template("errors/401.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return jsonify(error="Sorry, page not allowed.")
        return render_template("errors/403.html", error=error)

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return jsonify(error="Sorry, page not found.")
        return render_template("errors/404.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return jsonify("Sorry, an error has occured on our end.")
        return render_template("errors/500.html", error=error)

def configure_extensions(app):
    ''' Configure extensions '''
   
    FLASK_APP_DIR = os.path.dirname(os.path.abspath(__file__))

    db.init_app(app)
    asset = Environment(app)
    assets_output_dir = os.path.join(FLASK_APP_DIR, 'static', 'gen')
    if not os.path.exists(assets_output_dir):
        os.mkdir(assets_output_dir)
        
def configure_identity(app):
    ''' Configure middleware. '''
    
    principal = Principal(app)
    
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Get user identity from database
        # user = db.User.find()
        # for role in user.roles:
        #    identity.provides.add(RoleNeed(role.name))
        pass
    
    
def configure_logging(app):
    ''' Set up a debug and error log in log/ '''

    formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
            '[in %(pathname)s:%(lineno)d]')
    
    debug_handler = RotatingFileHandler('log/debug.log',
                                        maxBytes = 100000,
                                        backupCount = 10)

    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    app.logger.addHandler(debug_handler)

    error_handler = RotatingFileHandler('log/error.log',
                                        maxBytes = 100000,
                                        backupCount = 10)

    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    app.logger.addHandler(error_handler)
            
def configure_template_filters(app):
    ''' Make filters to be used in templates. '''

    @app.template_filter()
    def code_highlight(html):
        return helpers.code_highlight(html)
    
    @app.template_filter()
    def format_date(date):
        return helpers.format_date(date)
    
    @app.template_filter()
    def format_datetime(datetime):
        return helpers.format_datetime(datetime)
    
    @app.template_filter()
    def markup(text):
        return Markup(helpers.markup(text) or '')
    
    @app.template_filter()
    def timesince(dt):
        return helpers.timesince(dt)

    @app.template_filter()
    def truncate_html(html, num=25):
        return helpers.truncate_html_words(html, num)    

def generate_app(config):
    ''' Configures a variety of settings, extensions, and other bits and
    pieces for the app to be served.
    '''    
     
    ## Define the application object
    app = Flask(__name__, static_folder = 'static', template_folder = 'templates')
    app.config.from_object(config)
    
    configure_blueprints(app)
    configure_extensions(app)
    configure_logging(app)
    #configure_identity(app)
    configure_before_handlers(app)
    configure_template_filters(app)
    
    return app
