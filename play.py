#!/usr/bin/env python

from pprint import pprint
import random

def show(obj):
    '''Show the dump of the properties of the object.'''
    pprint(vars(obj))
    
import experientiarum
from experientiarum.config import DevConfig

from experientiarum import helpers
from experientiarum.extensions import * 

app = experientiarum.generate_app(DevConfig)

