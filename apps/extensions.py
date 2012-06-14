#!/usr/bin/env python

from flask.ext.admin import Admin
from flaskext.babel import Babel
from flaskext.bcrypt import Bcrypt
from flaskext.cache import Cache
from flaskext.mail import Mail
from flask.ext.mongokit import MongoKit

admin = Admin()
babel = Babel()
bcrypt = Bcrypt()
cache = Cache()
db = MongoKit()
mail = Mail()
