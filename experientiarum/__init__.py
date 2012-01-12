#!/usr/bin/env python

'''
    experientiarum
    
    ~ a place where I can leave my experiences

    @todo: explicitly define which apps are on/off
'''

__author__ = "Mark Feltner"
__copyright__ = "Copyright 2012, Mark Feltner"
__credits__ = ["Mark Feltner"]
__license__ = ""
__version__ = ""
__maintainer__ = "Mark Feltner"
__email__ = "feltner.mj@gmail.com"
__status__ = "Development"


import logging
import os

from logging import Formatter, FileHandler, StreamHandler
from logging.handlers import SMTPHandler

from flask import Flask, g, render_template
from flaskext.mongokit import MongoKit
from flaskext.assets import Environment


def generate_app(config):
    ''' Configures a variety of settings, extensions, and other bits and
    pieces for the app to be served.
     
    @TODO: More parameters for configuration overload
    @TODO: Procedurize; put operations in functions
    '''    
    
    FLASK_APP_DIR = os.path.dirname(os.path.abspath(__file__))
    
    ## Define the application object
    app = Flask(__name__, static_folder = 'static', template_folder = 'templates')
    app.config.from_object(config)
    
    ## Error Handling 
    # Logging
    '''
    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    app.logger.addHander(stream_handler)
    '''
    
    file_handler = FileHandler('log/experientarium.log')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)

    # Email
    """
    mail_handler = SMTPHandler('127.0.0.1',
                               'server-error@example.com',
                               ADMINS, '{ERROR!!!} [experientiarum]')
    mail_handler.setlevel(logging.ERROR)
    mail_handler.setFormatter(Formatter('''
    Message type:   %(levelname)s
    Location:       %(pathname)s:%(lineno)d
    Module:         %(module)s
    Function:       %(funcName)s
    Time:           %(asctime)s

    Message:

    %(message)s
    '''))
    app.logger.addHandler(mail_handler)
    """ 
    
    app.logger.info('%s config loaded from object' % config)
    
    
    ## Add MongoDB extension
    db = MongoKit(app)
    
    ## Webassets support
    assets = Environment(app)
    # Ensure output directory exists
    assets_output_dir = os.path.join(FLASK_APP_DIR, 'static', 'gen')
    if not os.path.exists(assets_output_dir):
        app.logger.info("webassets directory /static/gen not found. Creating it now.")
        os.mkdir(assets_output_dir)

    ## Register Blueprints
    # Main
    from main import main
    app.register_blueprint(main)
    app.logger.info('Main blueprint registered.')
    
    # BLOG
    from blog import blog
    app.register_blueprint(blog, url_prefix = '/blog')
    app.logger.info('Blog blueprint registered')

    from blog.models import Entry
    db.register([Entry])
    app.logger.info('Blog blueprint models registered with database.')
    
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
    
    @app.before_request
    def before_request():
        g.db = db
    
    app.logger.info('Application configured.')
    return app
