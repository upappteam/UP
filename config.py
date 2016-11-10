import os


# TODO Fix Database configurations in config.py file
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
        'password': '123'
                    },)
    ADMIN_2 = ({
        'name': 'majid',
        'family': 'mohamdi',
        'email': 'majid@gmail.com',
        'password': '123'
                    },)


class Develop(Config):
    DEBUG = True


class Deploy(Config):

    def init_app(app):
        Config.init_app(app)

config = {
    'develop': Develop,
    'deploy': Deploy,
}
