#!/usr/bin/env python

import os
import sys
import argparse

import logbook
from logbook import RotatingFileHandler, StreamHandler
from logbook.compat import RedirectLoggingHandler

from apps import generate_app


def configure_logging(app):
    ''' Set up a debug and error log in log/ '''

    
    app.logger.addHandler(RedirectLoggingHandler())
    logger_setup = logbook.NestedSetup([
        logbook.NullHandler(),
        # DEBUG Handler
        logbook.RotatingFileHandler(app.config['DEBUG_LOG'],
            level=logbook.DEBUG,
            max_size=100000,
            backup_count = 10),
        # ERROR Handler
        logbook.RotatingFileHandler(app.config['ERROR_LOG'],
            level=logbook.ERROR,
            max_size=100000,
            backup_count = 10),
        logbook.StreamHandler(sys.stdout, level=logbook.INFO),
        ])
        
    logger_setup.push_application()
    

def main(argv=None):
    ''' Main function to run the server '''

    if not argv:
        argv = 'settings.py'
    config = os.path.abspath(argv)
    
    app = generate_app(config)
    configure_logging(app)

    if app.debug:
        app.run('0.0.0.0')
    else:
        app.run()
    
    return 0

if __name__ == '__main__':
    status = main()
    sys.exit(status)
