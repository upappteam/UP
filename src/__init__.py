from flask import Flask
from flask_login import LoginManager

from config import config


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)

    from src.auth import bp_auth
    app.register_blueprint(bp_auth, url_prefix='/auth')

    from src.users import bp_user
    app.register_blueprint(bp_user, url_prefix='/users')

    from src.posts import bp_post
    app.register_blueprint(bp_post, url_prefix='/posts')

    from src.admin import bp_admin
    app.register_blueprint(bp_admin, url_prefix='/admin')

    from src.messages import bp_message
    app.register_blueprint(bp_message, url_prefix='/messages')

    return app
