#!/usr/bin/env python

from secret import super_secret_key, prod_mongo_user, \
    prod_mongo_pass

class Config():
    '''
    Default configuration values
    
    @todo: default index.html template
    '''
    
    SECRET_KEY = super_secret_key
    #INDEX_TEMPLATE = ''

class DevConfig(Config):
    
    TESTING = True
    DEBUG = True
    LOGGER_NAME = 'Dev. Logger'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    
class TestConfig(Config):
    
    TESTING = True
    LOGGER_NAME = 'Test. Logger'
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    
    
class ProdConfig(Config):
    ''' @todo: change MongoDB connections. '''
    
    DEBUG = False
    TESTING = False
    LOGGER_NAME = 'Prod. Logger'
    MONGODB_USERNAME = prod_mongo_user
    MONGODB_PASSWORD = prod_mongo_pass
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017