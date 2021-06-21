import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'testing_key')
    DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'PSBD_places')
    DATABASE_USER = os.environ.get('DATABASE_USER', 'postgres')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'postgres')
    DATABASE_PORT = os.environ.get('DATABASE_PORT', 5432)
    UPLOADED_PHOTOS_DEST = os.path.join(basedir, "app", "static", "photos")
