import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'strong key'

    @staticmethod
    def init_app(app):
        pass
#this is test

class Develop(Config):
    DEBUG = True


class Deploy(Config):

    def init_app(app):
        Config.init_app(app)

config = {
    'develop': Develop,
    'deploy': Deploy,
}