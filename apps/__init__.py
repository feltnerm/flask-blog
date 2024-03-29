#!/usr/bin/env python

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
import urlparse
import binascii

from flask import Flask, g, redirect, request, flash, render_template, url_for
    
from flask.ext.login import LoginManager

from apps import helpers
from apps.extensions import babel, bcrypt, cache, db

from apps.users import User

def setdefault(d, key, value):
    if d.get(key) is None:
        d[key] = value


def default_configuration(app):

    setdefault(app.config, 'PRODUCTION', True)
    setdefault(app.config, 'MONGODB_HOST', os.environ.get('MONGODB_HOST'))
    setdefault(app.config, 'MONGODB_PORT', int(os.environ.get('MONGODB_PORT')))
    setdefault(app.config, 'MONGODB_DATABASE', os.environ.get('MONGODB_DATABASE'))
    setdefault(app.config, 'MONGODB_USERNAME', os.environ.get('MONGODB_USERNAME'))
    setdefault(app.config, 'MONGODB_PASSWORD', os.environ.get('MONGODB_PASSWORD'))

    setdefault(app.config, 'CACHE_MEMCACHED_SERVERS', 
            ["%s:%s@%s" % (
                os.environ.get('MEMCACHE_USERNAME'), 
                os.environ.get('MEMCACHE_PASSWORD'),
                os.environ.get('MEMCACHE_SERVERS')
                    )
                ]
        )
    setdefault(app.config, 'SECRET_KEY', binascii.b2a_hqx(os.urandom(42)))


def configure_app(app, filename):
    """ Load the app's configuration. First, loads configuration defaults from 
    a pyfile, then overrides those defaults with what is found in the
    environment variables.
    """

    app.config.from_pyfile(filename)


def configure_assets(app):
    """ Set up Flask-Assets """

    assets = Environment(app)
    assets_output_dir = os.path.join(app.config['STATIC_ROOT'], 'gen')
    if not os.path.exists(assets_output_dir):
        os.mkdir(assets_output_dir)

    ## SITE REQUIRED
    # bootstrap
    #   /vendor/boostrap/js/bootstrap.min.js
    #   /vendor/bootstrap/css/

    bootstrap_wysihtml5_css = Bundle(
        'vendor/bootstrap/css/bootstrap-wysihtml5.css',
        filters='cssmin',
        output='gen/wysihtml5.css',
        )

    bootstrap_wysihtml5_js = Bundle(
        'vendor/bootstrap/js/bootstrap-wysihtml5-advanced.js',
        'vendor/bootstrap/js/wysihtml5.js',
        'vendor/bootstrap/js/bootstrap-wysihtml5.js',
        filters='rjsmin',
        output='gen/wysihtml5.js',
        )

    assets.register('js_base', 
            'vendor/bootstrap/js/bootstrap.min.js',
            'vendor/highlight/highlight.pack.js',
            'js/plugins.js',
            'js/script.js',
            filters='rjsmin',
            output='gen/packed.js',
            debug=app.debug
        )

    assets.register('css_base',
            'vendor/highlight/styles/github.css',
            'css/style.css',
            filters='cssmin',
            output='gen/packed.css',
            debug=app.debug
        )

    assets.register('bootstrap_wysihtml5_css', bootstrap_wysihtml5_css)
    assets.register('bootstrap_wysihtml_js', bootstrap_wysihtml5_js)


def configure_blueprints(app):
    ''' Register blueprints. '''
    
    # MAIN
    from main import main
    app.register_blueprint(main)
    
    # USERS
    from users import users
    app.register_blueprint(users)
    
    # BLOG
    from blog import blog
    app.register_blueprint(blog, url_prefix='/blog')

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
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            debugtoolbar = DebugToolbarExtension(app)
        except ImportError, e:
            pass


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
    login_manager.refresh_view = 'users.reauth'
    login_manager.needs_refresh_message = u'To protect your account, please reauthenticate to access this page.'

    ADMIN_USER = User(app.config['ADMIN_USERNAME']) 
    @login_manager.user_loader
    def load_user(username):
        if username == ADMIN_USER.username:
            return ADMIN_USER
        else:
            return None

    login_manager.setup_app(app)


def configure_logging(app):
    ''' Set up a debug and error log in log/ '''

    
    app.logger.addHandler(RedirectLoggingHandler())


def configure_template_filters(app):
    ''' Make filters to be used in templates. '''
    
    pass
#    @app.template_filter()
#    def code_highlight(html):
#


def generate_app(config):
    ''' Configures a variety of settings, extensions, and other bits and
    pieces for the app to be served.
    '''    
     
    ## Define the application object
    app = Flask(__name__, static_folder = 'static', template_folder = 'templates')
    
    configure_app(app, config)
    configure_logging(app)
    configure_extensions(app)
    configure_blueprints(app)
    configure_identity(app)
    configure_errorhandlers(app)
    configure_il8n(app)
    configure_template_filters(app)

    return app
