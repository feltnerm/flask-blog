#/usr/bin/env python

from datetime import datetime
from werkzeug import cached_property
from flask.ext.mongokit import Document

from apps.extensions import bcrypt, db

def authenticate(login, password):
    user = db.User.find_one({'_$or': [{'username':login}, {'email':login}]})

    if user:
        authenticated = user.check_password(password)
    else:
        authenticated = False

    return user, authenticated

def from_identity(identity):

    try:
        user = db.User.find_one(int(identity.name))
    except ValueError:
        user = None

    if user:
        identity.provides.update(user.provides)

    identity.user = user
    return user

def get_by_username(name):
    return db.User.find_one({'username':name})

class User(Document):
    ''' User model. Right now I only need an admin user that can
    add and edit apps posts, pastes, etc.
    
    @todo: add more users rather than just an admin
    '''
    
    __collection__ = 'users'
    
    CLASSES = {
            'member': 0,
            'moderator': 1,
            'admin': 2
            }

    structure = {
                 'username': unicode,
                 'password': unicode,
                 'email': unicode,
                 'date_joined': datetime,
                 'last_login': datetime,
                 'class': int
                 }
   
    required_fields = ['username','password']
    default_values = {
            'date_joined': datetime.utcnow(),
            'class': CLASSES['member']
            } 
    use_dot_notation = True
    
    def _get_password(self):
        return self.password
    
    def _set_password(self, password):
        self.password = unicode(bcrypt.generate_password_hash(password))
        
    def check_password(self, password):
        if not self.password:
            return False
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    
    @cached_property
    def provides(self):
        needs = [RoleNeed('authenticated'),
                UserNeed(self._id)]
        if self.is_moderator:
            needs.append(RoleNeed('moderator'))
        if self.is_admin:
            needs.append(RoleNeed('admin'))
        return needs

    @property
    def is_moderator(self):
        return self.get('class') >= self.CLASSES['moderator']

    @property
    def is_admin(self):
        return self.get('class') >= self.CLASSES['admin']

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self._id)
