#/usr/bin/env python

from datetime import datetime
from werkzeug import generate_password_hash, check_password_hash

from flaskext.mongokit import Document

from experientiarum.extensions import db

def get_by_username(name):
    return db.User.find_one({'username':name})

class User(Document):
    ''' User model. Right now I only need an admin user that can
    add and edit blog posts, pastes, etc.
    
    @todo: add more users rather than just an admin
    '''
    
    __collection__ = 'users'
    
    structure = {
                 'username': unicode,
                 'password': unicode,
                 'date_joined': datetime,
                 'last_login': datetime
                 }
   
    required_fields = ['username','password']
    default_values = {'date_joined': datetime.utcnow()} 
    use_dot_notation = True
    
    def __str__(self):
        return self.username
    
    def __repr__(self):
        return '<%s>' % self
    
    def _get_password(self):
        return self.password
    
    def _set_password(self, password):
        self.password = unicode(generate_password_hash(password))
        
    def check_password(self, password):
        if not self.password:
            return False
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
            
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self._id)
