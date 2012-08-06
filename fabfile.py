#!/usr/bin/env python

import binascii
import datetime
import os
import os.path
import platform
import urllib2
import urlparse
from pprint import pprint

import cssmin
from jinja2 import Environment, FileSystemLoader
from fabric.colors import *
from fabric.api import *
from fabric.contrib.console import *
from fabric.contrib.files import *
from fabric.utils import *

from flaskext.bcrypt import Bcrypt
bcrypt = Bcrypt()

"""
    fabfile

    Heavily inspired by: https://github.com/samuelclay/NewsBlur/blob/master/fabfile.py
"""


# ==============
# Color Printing
# ==============
def pblue(s, bold=False): 
    puts(blue(s,bold))
def pcyan(s, bold=False): 
    puts(cyan(s,bold))
def pgreen(s, bold=False): 
    puts(green(s, bold))
def pmage(s, bold=False): 
    puts(magenta(s,bold))
def pred(s, bold=False): 
    puts(red(s, bold))
def pwhite(s, bold=False): 
    puts(white(s, bold))
def pyellow(s, bold=False): 
    puts(yellow(s, bold))

@task
def penv():
    pblue("Current Environment:")
    pprint(env)


# ====================
# Environment Settings
# ====================

# Default
env.PROJECT_ROOT = os.path.dirname(__file__)
env.PROJECT_VENV = 'blog'
env.user = "mark"
env.roledefs = {
    'local': ['localhost'],
    'web': ['vivid-fire-8342.herokuapp.com']
    #'app': ['app.uwplatt.edu',
    #'dev': ['dev.uwplatt.edu'],
    #'ldap': ['ldap.uwplatt.ed'],
}

def server():
    env.PROJECT_ROOT = '/app/'

@task
def web():
    server()
    env.roles = ['web']

@task
def app():
    server()
    env.roles = ['app']

@task
def dev():
    server()
    env.roles = ['dev']

# ========
# Settings
# ========
def get_settings():

    settings = dict()
    # Prompt User for Settings
    pblue("Enter your environment settings.")
    settings['PRODUCTION'] = False
    if confirm(blue("Are these settings for a production server?")):
            settings['PRODUCTION'] = True

    puts('')
    pblue('##### ADMIN SETUP #####')
    settings['ADMIN_USERNAME'] = prompt(magenta('ADMIN_USERNAME:'))
    admin_password = prompt(magenta('ADMIN_PASSWORD:'))
    admin_password_hashed = bcrypt.generate_password_hash(admin_password)
    settings['ADMIN_PASSWORD_HASH'] = admin_password_hashed

    puts('')
    pblue('##### DATABASE SETUP #####')
    settings['MONGODB_HOST'] = prompt(magenta('MONGODB_HOST:'))
    settings['MONGODB_PORT'] = prompt(magenta('MONGODB_PORT:'))
    settings['MONGODB_DATABASE'] = prompt(magenta('MONGODB_DATABASE:'))
    settings['MONGODB_USERNAME'] = prompt(magenta('MONGODB_USERNAME:'))
    settings['MONGODB_PASSWORD'] = prompt(magenta('MONGODB_PASSWORD:'))

    puts('')
    pblue('##### MAIL SETUP #####')
    settings['MAIL_SERVER'] = prompt(magenta('MAIL_SERVER:'))
    settings['MAIL_PORT'] = prompt(magenta('MAIL_PORT:'))
    settings['MAIL_USERNAME'] = prompt(magenta('MAIL_USERNAME:'))
    settings['MAIL_PASSWORD'] = prompt(magenta('MAIL_PASSWORD:'))
    settings['MAILGUN_API_KEY'] = prompt(magenta('MAIL_API_KEY:')) 

    puts('')
    pblue('##### MEMCACHE SETUP #####')
    settings['MEMCACHE_SERVER'] = prompt(magenta('MEMCACHE_SERVER:'))
    settings['MEMCACHE_USERNAME'] = prompt(magenta('MEMCACHE_USERNAME:'))
    settings['MEMCACHE_PASSWORD'] = prompt(magenta('MEMCACHE_PASSWORD:'))
    secret_key = binascii.b2a_hqx(os.urandom(42)) 
    pred('\nSECRET KEY: %s' % secret_key)
    if confirm(yellow("Verify everything looks correct?")):
        settings['SECRET_KEY'] = secret_key
        return settings

    return None

@task
def make_local_settings():
    """ Creates a new settings.py (locally) """
    
    settings = get_settings()
    if settings:
        jenv = Environment(loader=FileSystemLoader('.'))
        text = jenv.get_template('settings.template.py').render(**settings or {})
        outputfile_name = 'settings.dev.py'
        with open(outputfile_name, 'w') as outputfile:
            outputfile.write(text)

@task
def make_settings():
    """ Creates a new settings.dev.py """
    settings = get_settings()
    if settings:
        outputfile_name = 'settings.dev.py'
        with cd(env.PROJECT_ROOT):
            with prefix('workon %s' % env.PROJECT_VENV): 
                upload_template('settings.template.py', 
                    os.path.join(env.PROJECT_ROOT, outputfile_name), 
                        context=settings, use_jinja=True, backup=False)

# ======================
# Environment Operations
# ======================
@task
def set_env():
    settings = get_settings()
    if settings:
        for key in settings:
            item = settings.get(key)
            if isinstance(item, bool):
                item = str(item)
            os.environ[key] = item
            local("export %s='%s'" % (key, item))
            print os.getenv(key)
@task
def make_venv():
    if run('python3 --version', True):
        run('mkproject -p python2.7 %s' % env.PROJECT_VENV)
    else:
        run('mkproject -p python2.7 %s' % env.PROJECT_VENV)


# ===================
# Development / Debug
# ===================
@task
def console():
    local('ipython -i play.py')

@task
def less():
    with lcd('apps/static/less'):
        local('lessc style.less ../css/style.css')

@task
def coffee():
    with lcd('apps/static/coffee'):
        local('coffee -b --compile --output ../js/ *.coffee')

@task
def uglify():
    with lcd('apps/static/js'):
        local('uglifyjs script.js >> script.min.js')
        local('uglifyjs plugins.js >> plugins.min.js')

@task
def cssmin():
    with lcd('apps/static/css'):
        local('cat *.css | cssmin > style.min.css')
@task
def watch_coffee():
    with lcd('apps/static/coffee'):
        local('coffee -o ../js/ --watch --compile ./*coffee')

@task
def build_assets():
    less()
    coffee()
    uglify()
    cssmin()

@task
def test():
    local('nosetest tests')


# ============
# Requirements
# ============
@task
def install_deps():
    """ Install dependencies depending on server type. """
    with prefix('source virtualenvwrapper.sh'):
        with prefix('workon %s' % env.PROJECT_VENV):
            if confirm(magenta("Is this a production server?")):
                run('pip install -U -r requirements/prod.txt --use-mirrors')
            else:
                run('pip install -U -r requirements/dev.txt --use-mirrors')

@task
def freeze():
    pass

# ===============
# Version Control
# ==============
@task
def clone():
    pass
    run('git clone git@github.com:feltnerm/blog.git %s' % env.PROJECT_ROOT)

@task
def commit():
    clean()
    build_assets()

    print "Commit message: "
    commit_message = raw_input()
    local("git commit -am \"%s\"" % commit_message)

@task
def pull():
    with cd(env.PROJECT_ROOT):
        run('git pull')

@task
@serial
def push():
    ''' Pushes local changes to master, and pulls them down to each server'''
    local('git push')
    with cd(env.PROJECT_ROOT):
        run('git pull')
@task
def status():
    s = local('git status --porcelain', True)
    if s:
        pyellow('Detected Changes to Branch', bold=True)
        puts(s)

# =====================
# Server Administration
# ====================


# ==========
# Migrations
# ==========


# ======
# Backups
# =======


# ===========
# Boilerplate
# ===========
@task
def boilerplate():
    """ Create a new project based on the boilerplate. """
    pgreen("Forging boilerplate.", bold=True)
    bp = dict()
    bp['SITE_NAME'] = prompt(magenta("Project Name: "))
    bp['PROJECT_ROOT'] = os.path.expanduser(os.path.join('~/Projects',bp['SITE_NAME']))
    if not confirm(green("%s okay for project root?" % bp['PROJECT_ROOT'])):
        bp['PROJECT_ROOT'] = prompt(magenta("Project Root: "))
    
    if not os.path.exists(bp['PROJECT_ROOT']):
        local('mkdir %s' % bp['PROJECT_ROOT'])
        local('cp -r %s/* %s' % (env.PROJECT_ROOT, bp['PROJECT_ROOT']))
        #upload_template('settings.py.template',
        #    bp['PROJECT_ROOT'],
        #    context=bp,
        #    use_jinja=True,
        #    backup=False
        #    )
    else:
        pred('Project already exists!')

# =========
# Deployment
# =========
@task
def bootstrap():

    pgreen("Bootstrappin' yer server!", bold=True)
    #make_venv()
    #install_deps()
    #pull()
    #init_postgres()
    #init_mongo()
    #make_settings()
    #init_migrate()
    
    #with cd(env.PROJECT_ROOT):
        #run('mkdir log/')
    
@task
def deploy():
    clean()
    build_assets()
    local('git push origin master')
    local('git push heroku master')

# ===============
# Setup :: Common
# ===============

# =========
# Utilities
# =========
@task
def clean():
    rmpyc()
    with lcd('apps/static/'):
        local('rm -rf js/*.js')
        local('rm -rf css/*.css')
        local('rm -rf gen/*')

@task
def pychecker():
    local('pychecker .')

@task
def pep8():
    """ Run PEP8 on my code. """
    puts("Checking python style")
    with cd(env.PROJECT_ROOT):
        local('pep8 .')
@task
def rmpyc():
    ''' Delete compiled python (.pyc) files. '''

    pwhite('Removing .pyc files.')
    local("find . -iname '*.pyc' -exec rm -v {} \;", capture=False)
