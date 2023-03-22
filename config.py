# -*- encoding: utf-8 -*-

import os


class Config(object):

    HOST_URL = os.environ.get('HOST_URL')
    SERVER_NAME = os.environ.get('SERVER_NAME')

    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    WTF_CSRF_TIME_LIMIT = None

    LANGUAGES = ['en', 'fr', 'ar']
    UPLOADED_DOCUMENTS_DEST = os.environ.get('UPLOADED_DOCUMENTS_DEST')
    UPLOADED_IMAGES_DEST = os.environ.get('UPLOADED_IMAGES_DEST')
    UPLOADED_PICTURES_DEST = os.environ.get('UPLOADED_PICTURES_DEST')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_PROD_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DebugConfig(Config):
    DEBUG = True


config_dict = {
    'Production': ProductionConfig,
    'Development': DevelopmentConfig,
    'Debug': DebugConfig
}
