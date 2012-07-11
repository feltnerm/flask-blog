#!/usr/bin/env python

import sys
import os
import os.path
import logging
import binascii

# ================
# Server Settings
# ================

SITE_NAME = 'encephalo' #ENTER SITE NAME!
SITE_URL = 'encephalo.herokuapp.com'
#ADMINS = []
#SERVER_EMAIL = ''


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
VENDOR_ROOT = os.path.join(CURRENT_DIR, 'vendor')

# ===========
# Python Path
# ===========
if '/helpers' not in ''.join(sys.path):
    sys.path.append(HELPERS_ROOT)
if '/vendor' not in ''.join(sys.path):
    sys.path.append(VENDOR_ROOT)

# ===============
# Global Settings
# ===============
PRODUCTION = False 
DEVELOPMENT = not PRODUCTION

DEBUG = not PRODUCTION
TESTING = DEBUG
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'utc'
ASSETS_DEBUG = DEBUG
INDEX_TEMPLATE = 'index.html'
SECRET_KEY = """L+ZMKh"622)&X(r`"iTL&)#@&#4+'f&%UKQY@cP)r$U`*XZ&E6C)IaaX"""

# =======
# Logging
# =======
LOG_LEVEL = logging.DEBUG
LOGGER_NAME = SITE_NAME
LOG_DIR = os.path.join(CURRENT_DIR, 'log')
LOGFILE = os.path.join(LOG_DIR, '%s.log' % SITE_NAME) # ENTER APP NAME
DEBUG_LOG = os.path.join(LOG_DIR, 'debug.log')
ERROR_LOG = os.path.join(LOG_DIR, 'error.log')

# ====
# Mail
# ====
MAIL_SERVER = ''
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_DEBUG = DEBUG

# =======
# MongoDB
# =======
MONGODB_DATABASE = 'blog'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_USERNAME = ''
MONGODB_PASSWORD = ''
# =====
# Cache
# =====
CACHE_TYPE = 'null'
#CACHE_DEFAULT_TIMEOUT = 300
#CACHE_TYPE = 'memcached'
#CACHE_MEMCACHED_SERVERS = [':']
#CACHE_MEMCACHED_SERVERS = [os.environ.get('MEMCACHE_USERNAME')+':'+os.environ.get('MEMCACHE_PASSWORD')+'@'+os.environ.get('MEMCACHE_SERVER'),]
