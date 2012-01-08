#!/usr/bin/env python


class Config():
    '''
    Default configuration values
    '''
    SECRET_KEY = ''

class DevelopmentConfig(Config):
    
    DEBUG = True
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017    

class ProductionConfig(Config):
    
    DEBUG = False