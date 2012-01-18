#!/usr/bin/env python

from secret import super_secret_key, prod_mongo_user, prod_mongo_pass

class Config():
    '''
    Default configuration values
    
    @todo: default index.html template
    @todo: Parameterized Configuration class
    '''
    
    ADMINS = ['feltner.mj@gmail.com']
    LOGGER_NAME = 'experientarium log'
    SITE_NAME = 'experientiarum'
    SECRET_KEY = super_secret_key
    INDEX_TEMPLATE = 'index.html'

class DevConfig(Config):
    
    SITE_NAME = Config.SITE_NAME + ' - development'
    TESTING = True
    DEBUG = True
    MONGODB_DATABASE = 'devdb'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    
class TestConfig(Config):
    
    SITE_NAME = Config.SITE_NAME + ' - testing'
    TESTING = True
    MONGODB_DATABASE = 'testdb'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    
    
class ProdConfig(Config):
    ''' @todo: change MongoDB connections. '''
    
    SITE_NAME = 'experientiarum'
    DEBUG = False
    TESTING = False
    MONGODB_DATABASE = 'proddb'
    MONGODB_USERNAME = prod_mongo_user
    MONGODB_PASSWORD = prod_mongo_pass
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
