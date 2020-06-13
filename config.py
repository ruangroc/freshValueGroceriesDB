import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # heroku database
    DATABASE_URL = os.environ.get('DATABASE_URL')