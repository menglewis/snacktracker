import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SECRET_KEY = "devtestkey"

#CELERY_BROKER_URL = ""
#CELERY_RESULT_BACKEND = ""