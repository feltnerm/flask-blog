#!/usr/bin/env python

import os
import random
import readline

from pprint import pprint

from flask import *

import experientiarum
from experientiarum.config import DevConfig

from experientiarum import helpers
from experientiarum.extensions import *

app = experientiarum.generate_app(DevConfig)

os.environ['PYTHONINSPECT'] = 'True'

def show(obj):
    '''Show the dump of the properties of the object.'''
    pprint(vars(obj))
