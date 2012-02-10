#!/usr/bin/env python

from logbook import NestedSetup, NullHandler, RotatingFileHandler, Processor 
from flaskext.mongokit import MongoKit

db = MongoKit()

log = NestedSetup([
            NullHandler(),
            RotatingFileHandler('log/warning.log', level='WARNING'),
            RotatingFileHandler('log/error.log', level='ERROR'),
            RotatingFileHandler('log/debug.log', level='DEBUG'),
    ])
