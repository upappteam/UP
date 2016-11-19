from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager

from config import config
from src.utils.models import Utils
from src.users.models import User


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

    @app.route('/')
    def index():
        return render_template('index.html')

    from config import Admin as ADMINS
    from src.admin.models import Admin

    @app.before_first_request
    def init_admin():
        admin1 = Admin(name=ADMINS.ADMIN_1[0]['name'],
                       family=ADMINS.ADMIN_1[0]['family'],
                       email=ADMINS.ADMIN_1[0]['email'],
                       password=Utils.set_password(ADMINS.ADMIN_1[0]['password']),
                       permission=ADMINS.ADMIN_1[0]['permission']
                       )

        admin2 = Admin(name=ADMINS.ADMIN_2[0]['name'],
                       family=ADMINS.ADMIN_2[0]['family'],
                       email=ADMINS.ADMIN_2[0]['email'],
                       password=Utils.set_password(ADMINS.ADMIN_2[0]['password']),
                       permission=ADMINS.ADMIN_2[0]['permission']
                       )

        admin1.init_neo4j()
        admin2.init_neo4j()

    @login_manager.user_loader
    def user_loader(user_id):
        if user_id is None:
            return redirect(url_for("auth.login"))

        user = User.find_by_id(user_id)
        admin_data = Admin.find_admin_id(user_id)
        if admin_data:
            admin = Admin.classify(name=admin_data["name"],
                                   family=admin_data["family"],
                                   email=admin_data["email"],
                                   password=admin_data["password"],
                                   permission=admin_data["permission"],
                                   _id=admin_data["_id"])
            return admin
        if user:
            return user

    return app
