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
import sys

from flask import Flask, g, redirect, request, flash,  Markup, render_template, url_for
    
from flask.ext.assets import Environment, Bundle
from flask.ext.login import LoginManager
from flask.ext.principal import Principal, RoleNeed, UserNeed, identity_loaded

import logbook
from logbook import RotatingFileHandler, StreamHandler
from logbook.compat import RedirectLoggingHandler

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

    bootstrap_wysihtml5_css = Bundle(
        'vendor/bootstrap/css/bootstrap-wysihtml5.css',
        filters='cssmin',
        output='gen/wysihtml5.css',
        debug=app.debug
        )

    bootstrap_wysihtml5_js = Bundle(
        'vendor/bootstrap/js/bootstrap-wysihtml5-advanced.js',
        'vendor/bootstrap/js/wysihtml5.js',
        'vendor/bootstrap/js/bootstrap-wysihtml5.js',
        filters='jsmin',
        output='gen/wysihtml5.js',
        debug=app.debug
        )

    bootstrap_js = Bundle(
        'vendor/bootstrap/js/bootstrap.min.js',
        filters='jsmin')

    script_js = Bundle(
        'coffee/script.coffee',
        filters='coffeescript',
        output='js/script.js',
        debug=False)

    style_less = Bundle(
        'less/style.less',
        filters='less',
        output='css/style.css',
        debug=False)

    assets.register('js_base', bootstrap_js, script_js,
        Bundle(
            os.path.join(app.config['STATIC_ROOT'], 'vendor/highlight/highlight.pack.js')
            ),
        filters='jsmin',
        output='gen/packed.js',
        debug=app.debug)

    assets.register('css_base', 'css/style.css',
        Bundle('vendor/highlight/styles/github.css'),
        filters='cssmin',
        output='gen/packed.css',
        debug=app.debug)

    assets.register('bootstrap_wysihtml5_css', bootstrap_wysihtml5_css)
    assets.register('bootstrap_wysihtml_js', bootstrap_wysihtml5_js)

    app.logger.info('Assets Registered')


def configure_beforehandlers(app):

    @app.before_request
    def authenticate():
        app.logger.debug('UserAuth: %s' % g.identity)
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

    app.logger.info('Blueprints and models registered.')

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
        app.logger.error('Server Error! %s' % error)
        return render_template("errors/500.html", error=error)

def configure_extensions(app):
    ''' Configure extensions '''
   
    bcrypt.init_app(app)
    babel.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    if app.debug:
        from flask_debugtoolbar import DebugToolbarExtension
        debugtoolbar = DebugToolbarExtension(app)

    app.logger.info('Extensions initialized')

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
        app.logger.debug('User Identity Loaded: %s' % identity.name)
        user = db.User.find_one({"username": identity.name})
        identity.provides.add(RoleNeed(user.role))
        identity.user = user
        g.user = user

    @login_manager.user_loader
    def load_user(userid):
        app.logger.debug('User Session Loaded: %s' % helpers.to_oid(userid))
        return db.User.get_from_id(helpers.to_oid(userid))

    login_manager.setup_app(app)

    app.logger.info('Identity Management Initialized')

def configure_logging(app):
    ''' Set up a debug and error log in log/ '''

    
    app.logger.addHandler(RedirectLoggingHandler())
    logger_setup = logbook.NestedSetup([
        logbook.NullHandler(),
        # DEBUG Handler
        #logbook.RotatingFileHandler(app.config['DEBUG_LOG'],
        #    level=logbook.DEBUG,
        #    max_size=100000,
        #    backup_count = 10),
        # ERROR Handler
        #logbook.RotatingFileHandler(app.config['ERROR_LOG'],
        #    level=logbook.ERROR,
        #    max_size=100000,
        #    backup_count = 10),
        logbook.StreamHandler(sys.stdout, level=logbook.INFO),
        ])
        
    logger_setup.push_application()

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
    app.logger.debug('%s warming up' % app.config['SITE_NAME'])
    app.logger.debug('Configuration used: %s' % config)
    configure_blueprints(app)
    configure_extensions(app)
    configure_assets(app)
    configure_identity(app)
    configure_errorhandlers(app)
    configure_il8n(app)
    configure_template_filters(app)
    return app
