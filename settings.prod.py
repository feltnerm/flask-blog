#!/usr/bin/env python

import sys
import os
import os.path
import logging
import binascii
import urlparse

# ================
# Server Settings
# ================

SITE_NAME = 'encephalo' #ENTER SITE NAME!
#SITE_URL = 'encephalo.herokuapp.com'
#ADMINS = []
#SERVER_EMAIL = None


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

# =======
# Logging
# =======
LOG_LEVEL = logging.DEBUG
LOGGER_NAME = SITE_NAME

# ====
# Mail
# ====
MAIL_DEBUG = DEBUG

# =======
# MongoDB
# =======

# =====
# Cache
# =====
CACHE_TYPE = 'null'
CACHE_DEFAULT_TIMEOUT = 300
#CACHE_TYPE = 'memcached'
#CACHE_MEMCACHED_SERVERS = [os.environ.get('MEMCACHE_USERNAME')+':'+os.environ.get('MEMCACHE_PASSWORD')+'@'+os.environ.get('MEMCACHE_SERVERS'),]
