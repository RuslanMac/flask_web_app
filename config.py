import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app2.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WORDS_PER_PAGE = 20
    YANDEX_DICTIONARY_KEY = os.environ.get('YANDEX_DICTIONARY_KEY')
    LANGUAGES = ['en','ru']