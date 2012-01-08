#!/usr/bin/env python
import platform

import os
import datetime
import urllib2

from fabric.api import env, roles, local, sudo, run, hide
from fabric import colors
from fabric.utils import puts, warn

## Run things
def console():
    ''' Open interactive console '''
    local('ipython -i play.py', capture=False)

def server():
    '''Run the dev server'''
    local('env DEV=yes python runserver.py', capture=False)

def test():
    '''Run the test suite'''
    local('env TEST=yes python tests.py', capture=False)


## Deployment
def pack():
    ''' Pack up code '''
    pass    

def unpack():
    ''' Unpack code '''
    pass


## Utils
def pep8():
    ''' Flags any violations of the python style guide '''
    print("Checking python style")
    # Grab everything public folder inside the current directory
    dir_list = [x[0] for x in os.walk('./') if not x[0].startswith('./.')]
    # Loop through them all and run pep8
    results = []
    with hide('everything'):
        for d in dir_list:
            results.append(local("pep8 %s" % d))
    # Filter out the empty results and print the real stuff
    results = [e for e in results if e]
    for e in results:
        print(e)

def clear_pyc():
    ''' Clear cached .pyc files '''
    local("find . -iname '*.pyc' -exec rm -v {} \;", capture=False)