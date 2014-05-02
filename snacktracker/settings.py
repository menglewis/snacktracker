import os

class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(APP_DIR, '../test.sqlite')
    DEBUG = True

class ProdConfig(Config):
    '''Production configuration.'''
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = False

class DevConfig(Config):
    '''Development configuration.'''
    SECRET_KEY = 'devsecretkey'

class TestingConfig(Config):
    SECRET_KEY = 'testsecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False