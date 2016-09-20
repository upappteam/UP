from flask import Flask
from flask_login import LoginManager

from config import config
from src.auth import bp_auth
from src.users import bp_user
from src.posts import bp_post
from src.messages import bp_message


# TODO Fix the configurations

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'users.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)

    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_user, url_prefix='/users')
    app.register_blueprint(bp_post, url_prefix='/posts')
    app.register_blueprint(bp_message, url_prefix='/messages')

    return app
