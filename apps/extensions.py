#!/usr/bin/env python

from flaskext.babel import Babel
from flaskext.bcrypt import Bcrypt
from flaskext.cache import Cache
from flask.ext.mongokit import MongoKit

babel = Babel()
bcrypt = Bcrypt()
cache = Cache()
db = MongoKit()
