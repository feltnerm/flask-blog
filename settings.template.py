#!/usr/bin/env python

"""
  A lot of these settings are generate via the fabfile. Check out
  make_settings in there.

  i.e., 
  $ fab make_settings

  or

  $ fab make_local_settings

""" 


import sys
import os
import os.path
import logging
import binascii

# ================
# Server Settings
# ================

SITE_NAME = '' 
SITE_URL = ''
ADMIN_USERNAME = '{{ ADMIN_USERNAME }}'
ADMIN_PASSWORD_HASH = """{{ ADMIN_PASSWORD_HASH}}"""


# ======================
# Directory Declarations
# ======================

CURRENT_DIR = os.path.dirname(__file__)
APPS_ROOT = os.path.join(CURRENT_DIR, 'apps')
APPS_DIRS = (
    os.path.join(APPS_ROOT, 'blog'),
    os.path.join(APPS_ROOT, 'bookmarks'),
    os.path.join(APPS_ROOT, 'main'),
    os.path.join(APPS_ROOT, 'pastebin'),
    os.path.join(APPS_ROOT, 'readlaters'),
    os.path.join(APPS_ROOT, 'todo'),
    os.path.join(APPS_ROOT, 'users')
        )
TEMPLATE_DIRS = (os.path.join(APPS_ROOT, 'templates'), )
STATIC_ROOT = os.path.join(APPS_ROOT, 'static')
HELPERS_ROOT = os.path.join(CURRENT_DIR, 'helpers')


# ===========
# Python Path
# ===========
if '/helpers' not in ''.join(sys.path):
    sys.path.append(HELPERS_ROOT)


# ===============
# Global Settings
# ===============
PRODUCTION = {{ PRODUCTION }} 
DEVELOPMENT = not PRODUCTION

DEBUG = not PRODUCTION
TESTING = DEBUG
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'utc'
ASSETS_DEBUG = DEBUG
INDEX_TEMPLATE = 'index.html'
SECRET_KEY = """{{ SECRET_KEY }}"""


# =======
# Logging
# =======
LOG_LEVEL = logging.DEBUG
LOGGER_NAME = SITE_NAME
LOG_DIR = os.path.join(CURRENT_DIR, 'log')
LOGFILE = os.path.join(LOG_DIR, '%s.log' % SITE_NAME) # ENTER APP NAME
DEBUG_LOG = os.path.join(LOG_DIR, 'debug.log')
ERROR_LOG = os.path.join(LOG_DIR, 'error.log')


# =======
# MongoDB
# =======
MONGODB_DATABASE = '{{ MONGODB_DATABASE }}'
MONGODB_HOST = '{{ MONGODB_HOST }}'
MONGODB_PORT = {{ MONGODB_PORT }}
MONGODB_USERNAME = '{{ MONGODB_USERNAME }}'
MONGODB_PASSWORD = '{{ MONGODB_PASSWORD }}'


# =====
# Cache
# =====
CACHE_TYPE = 'null'
#CACHE_DEFAULT_TIMEOUT = 300
#CACHE_TYPE = 'memcached'
#CACHE_MEMCACHED_SERVERS = [os.environ.get('MEMCACHE_USERNAME')+':'+os.environ.get('MEMCACHE_PASSWORD')+'@'+os.environ.get('MEMCACHE_SERVERS'),]
