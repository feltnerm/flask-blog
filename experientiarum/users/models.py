#!/usr/bin/env python

from datetime import datetime

from flaskext.mongokit import Document
from flaskext.principal import RoleNeed, UserNeed, Permission

from experientiarum.extensions import db
from experientiarum.permissions import admin


class User(Document):
    ''' User model. Right now I only need an admin user that can
    add and edit blog posts, pastes, etc.
    
    @todo: add more users rather than just an admin
    '''
    
    __collection__ = 'users'
    
    MEMBER = 100
    MODERATOR = 200
    ADMIN = 300
    
    structure = {
                 'username': unicode,
                 'password_hash': unicode,
                 'email': unicode,
                 'role': int,
                 }
    required_fields = ['username','password','role']
    default_values = {'role':MEMBER}
    use_dot_notation = True
    