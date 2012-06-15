#!/usr/bin/env python

import sys
import os
import os.path
import logging

# ================
# Server Settings
# ================

SITE_NAME = 'experientiarum' #ENTER SITE NAME!
#SITE_URL = ''
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
LOGFILE = os.path.join(CURRENT_DIR, 'log/%s.log' % SITE_NAME) # ENTER APP NAME

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
SECRET_KEY = """&4CJl2JE,2-8EX6$HGI0p!2R4b+A6NE5E43UQ5CaCPTP4hVUAe(01FEa"""

# =======
# Logging
# =======
LOG_LEVEL = logging.DEBUG
LOGGER_NAME = SITE_NAME
DEBUG_LOG = 'logs/debug.log'
ERROR_LOG = 'logs/error.log'

# ====
# Mail
# ====
#MAIL_SERVER = ''
#MAIL_PORT = 
#MAIL_USERNAME = ''
#MAIL_PASSWORD = ''
#DEFAULT_MAIL_SENDER = ''
#MAIL_DEBUG = DEBUG

# =======
# MongoDB
# =======
MONGODB_DATABASE = 'experientiarum'
MONGODB_USERNAME = ''
MONGODB_PASSWORD = ''
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# =====
# Cache
# =====
CACHE_TYPE = 'null'
CACHE_DEFAULT_TIMEOUT = 300
#CACHE_TYPE = 'memcached'
#CACHE_MEMCACHED_SERVERS = [':']