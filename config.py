import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'testing_key'
    DATABASE_HOST = os.environ.get('DATABASE_HOST') or 'localhost'
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'PSBD_places'
    DATABASE_USER = os.environ.get('DATABASE_USER') or 'postgres'
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD') or 'postgres'
    DATABASE_PORT = os.environ.get('DATABASE_PORT') or 5432
