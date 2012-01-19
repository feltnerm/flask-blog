#!/usr/bin/env python

from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash

from flaskext.mongokit import Document
from flaskext.principal import RoleNeed, UserNeed, Permission

from experientiarum.extensions import db
from experientiarum.permissions import admin, moderator

def authenticate(login, password):
    
    user = db.User.find_one({"username":login})
    
    if user:
        authenticated = user.check_password(password)
    else:
        authenticated = False
    
    return user, authenticated

def get_by_identity(identity):
    
    users = 

def get_by_username(username):
    return db.User.find_one_or_404({"username":username})

def search(keywords):
    pass
     
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
                 'password': unicode,
                 'role': int,
                 'date_joined': datetime,
                 'last_login': datetime
                 }
    required_fields = ['username','password']
    default_values = {'date_joined': datetime.utcnow(), 
                      'role':MEMBER}
    use_dot_notation = True
    
    def __str__(self):
        return self.username
    
    def __repr__(self):
        return '<%s>' % self
    
    def _get_password(self):
        return self.password
    
    def _set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        if not self.password:
            return False
        return check_password_hash(self.password, password)
    
    @property
    def is_moderator(self):
        return self.role >= self.MODERATOR
    
    @property
    def is_admin(self):
        return self.role >= self.ADMIN   
