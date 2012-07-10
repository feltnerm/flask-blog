#!/usr/bin/env python

import sys
import os
import os.path
import logging

# ================
# Server Settings
# ================

SITE_NAME = 'experientiarum' #ENTER SITE NAME!
SITE_URL = ''
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
PRODUCTION = True
DEVELOPMENT = not PRODUCTION

DEBUG = not PRODUCTION
TESTING = DEBUG
BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = 'utc'
ASSETS_DEBUG = DEBUG
INDEX_TEMPLATE = 'index.html'
SECRET_KEY = """e)FpKGR-lakI4M+lXPLHdFUD0b6!&,(TlHY2XQ6T&D[#haQU)J,HVp!i"""

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
MAIL_SERVER = 'smtp.mailgun.org'
MAIL_USERNAME = 'postmaster@app5809676.mailgun.org'
MAIL_PASSWORD = '9xlp0hl9xiq0'
MAIL_API_KEY = 'key-3bh8scnsdpibkumo83ir1t7ynswizmt6'
MAIL_DEBUG = DEBUG

# =======
# MongoDB
# =======
MONGODB_DATABASE = 'heroku_app5809676'
MONGODB_USERNAME = 'heroku_app5809676'
MONGODB_PASSWORD = 'k8vaht13in9q55i1i6hi6cq968'
MONGODB_HOST = 'ds035607-a.mongolab.com'
MONGODB_PORT = 35607

# =====
# Cache
# =====
#CACHE_TYPE = 'null'
CACHE_DEFAULT_TIMEOUT = 300
CACHE_TYPE = 'memcached'
#CACHE_MEMCACHED_SERVERS = [':']
CACHE_MEMCACHED_SERVERS = ['app5809676%40heroku.com:AP+fzP2q3svbbmnU@:',]