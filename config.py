import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'strong key'

    @staticmethod
    def init_app(app):
        pass


class Admin:

    ADMIN_1 = ({
        'name': 'mohamad',
        'family': 'hasani',
        'email': 'mohamad@gmail.com',
        'password': '123',
        'permission': 0x80
                    },)
    ADMIN_2 = ({
        'name': 'majid',
        'family': 'mohamdi',
        'email': 'majid@gmail.com',
        'password': '123',
        'permission': 0x80
                    },)


class Develop(Config):
    DEBUG = True
    URI = '0.0.0.0:7474/db/data'
    SECURE = False


class Deploy(Config):
    DEBUG = False
    SECURE = True
    HOST = None  # TODO Fix host for deploy
    PORT = None  # TODO Fix port for deploy
    USERNAME = None  # TODO Fix user (user name) for deploy
    PASSWORD = None  # TODO Fix password for deploy

    def init_app(app):
        Config.init_app(app)

config = {
    'develop': Develop,
    'deploy': Deploy,
    'default': Develop
}
