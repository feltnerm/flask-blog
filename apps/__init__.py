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

from flask import Flask, g, redirect, request, flash,  Markup, render_template, url_for
    
from flask.ext.assets import Environment, Bundle
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager
from flask.ext.principal import Principal, RoleNeed, UserNeed, identity_loaded

from apps import helpers
from apps.extensions import admin, babel, bcrypt, cache, db, mail
from apps.users.models import from_identity

def configure_app(app, filename):
    """ Load the app's configuration. """
    app.config.from_pyfile(filename)


def configure_assets(app):
    """ Set up Flask-Assets """

    assets = Environment(app)
    assets_output_dir = os.path.join(app.config['STATIC_ROOT'], 'gen')
    if not os.path.exists(assets_output_dir):
        os.mkdir(assets_output_dir)

    less_css = Bundle('less/style.less',
            filters='less',
            output='css/style.css',
            debug=False)

    coffee_script = Bundle('coffee/script.coffee',
            filters='coffeescript',
            output='gen/script.js',
            debug=False)

    assets.register('css_all', less_css,
            filters='cssmin',
            output='css/style.css',
            debug=app.debug)

    assets.register('js_all', coffee_script,
            filters='uglifyjs',
            output='js/script.js',
            debug=app.debug)


def configure_beforehandlers(app):

    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)

def configure_blueprints(app):
    ''' Register blueprints. '''
    
    # MAIN
    from main import main
    app.register_blueprint(main)
    
    # USERS
    from users import users
    app.register_blueprint(users)
    
    from users.models import User
    db.register([User])
        
    # BLOG
    from blog import blog
    app.register_blueprint(blog, url_prefix = '/blog')

    from blog.models import Entry
    db.register([Entry])
    
    # BOOKMARKS
    #from bookmarks import bookmarks
    #app.register_blueprint(bookmarks, url_prefix = '/bookmarks')
    
    # PASTEBIN
    #from pastebin import pastebin
    #app.register_blueprint(pastebin, url_prefix = '/pastebin')

    #from pastebin.models import Paste
    #db.register([Paste])
    
    # READLATERS
    #from readlaters import readlaters
    #app.register_blueprint(readlaters, url_prefix = '/readlaters')
    
    # TODO
    #from todo import todo
    #app.register_blueprint(todo, url_prefix = '/todo')


def configure_errorhandlers(app):
    ''' Set up default HTTP error pages '''

    @app.errorhandler(401)
    def unauthorized(error):
        return redirect(url_for('users.login', next=request.path))

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html", error=error)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        return render_template("errors/500.html", error=error)

def configure_extensions(app):
    ''' Configure extensions '''
   
    bcrypt.init_app(app)
    babel.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    if app.debug:
        debugtoolbar = DebugToolbarExtension(app)

def configure_il8n(app):
    """ Configure internationalization with Flask-Babel. """
    @babel.localeselector
    def get_locale():
        accept_languages = app.config('ACCEPT_LANGUAGES', ['en'])
        return request.accept_languages.best_match(accept_languages)


def configure_identity(app):
    ''' Configure middleware. '''
   
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.login_message = u'Please log in to access this page.'
    #login_manager.refresh_view = 'users.reauth'
    #login_manager.needs_refresh_message = u'To protect your account, please reauthenticate to access this page.'

    principal = Principal(app)
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        user = db.User.find_one({"username": identity.name})
        identity.provides.add(RoleNeed(user.role))
        identity.user = user
        g.user = user

    @login_manager.user_loader
    def load_user(userid):
        return db.User.get_from_id(helpers.to_oid(userid))

    login_manager.setup_app(app)

def configure_logging(app):
    ''' Set up a debug and error log in log/ '''

    formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
            '[in %(pathname)s:%(lineno)d]')
    
    if app.debug:
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
    
    info_handler = StreamHandler(logging.INFO)
    info_handler.setFormatter(formatter)
    app.logger.addHandler(info_handler)

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
    def gfm(text):
        return Markup(helpers.githubmarkdown(text) or '')

    @app.template_filter()
    def markup(text, style=None):
        return Markup(helpers.markup(text, style = style) or '')
    
    @app.template_filter()
    def timesince(dt):
        return helpers.timesince(dt)

    @app.template_filter()
    def truncate_html(html, num=200):
        return helpers.truncate_html_words(html, num)    

def generate_app(config):
    ''' Configures a variety of settings, extensions, and other bits and
    pieces for the app to be served.
    '''    
     
    ## Define the application object
    app = Flask(__name__, static_folder = 'static', template_folder = 'templates')
    
    configure_app(app, config)
    configure_logging(app)
    configure_blueprints(app)
    configure_extensions(app)
    configure_assets(app)
    configure_identity(app)
    configure_errorhandlers(app)
    configure_il8n(app)
    configure_template_filters(app)
    return app
