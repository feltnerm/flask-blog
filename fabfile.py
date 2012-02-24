#!/usr/bin/env python

import datetime
import os
import platform
import urllib2

from fabric import colors
from fabric.api import *
from fabric.utils import puts, warn


## Run things
def console():
    ''' Open interactive console '''
    
    local('ipython -i play.py', capture=False)

def server():
    ''' Run the development server'''
    
    local('python runserver.py --server-type d', capture=False)

def test():
    '''Run the test suite'''
    
    local('python tests.py', capture=False)

## Deployment
PROJECT_ROOT = os.path.abspath('../')
PROJECT_NAME = os.path.basename(PROJECT_ROOT)

def ec2():
    env.hosts = ['23.21.160.20']
    env.user = 'ubuntu'
    env.key_filename = '/home/mark/.ssh/webserverkey.pem'

def pack():
    ''' @todo: Pack up code '''    
    #local('cd %s' % PROJECT_DIRECTORY)
    #local('tar -cf %s.tar %s' % (PROJECT_NAME, PROJECT_NAME)
    #local('gzip %s.tar' % PROJECT_NAME) 
    pass

def unpack():
    ''' @todo: Unpack code '''
    pass 

def update():
    ''' Update local copy from master remote git repo. '''
    
    run('git pull origin master')
    
def install_deps():
    ''' Install python dependencies. '''
    
    run('pip install -q -r requirements.txt')

## Utils
def lessc():
    ''' compiles .less -> .css with lessc '''
    
    local('lessc experientiarum/static/css/site.less experientiarum/static/css/site.css')

def pychecker():
    ''' Checks code with pychecker '''
    
    local('pychecker .')

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

def tabnanny():
    ''' Checks whether any of the input files have improper tabs. '''

    print('Running tabnanny')
    with hide('everything'):
        local('python -m tabnany ./')

def rmpyc():
    ''' Clear cached .pyc files '''
    
    print("Removing .pyc files.")
    local("find . -iname '*.pyc' -exec rm -v {} \;", capture=False)
