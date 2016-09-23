from flask import render_template, redirect, url_for

from src import create_app, login_manager
from src.users.models import User
from src.admin.models import Admin
from config import Admin as ADMINS


app = create_app('develop')


@app.before_first_request
def init_admins():
    admin1 = Admin(ADMINS.ADMIN_1[0]['name'],
                   ADMINS.ADMIN_1[0]['family'],
                   ADMINS.ADMIN_1[0]['email'],
                   ADMINS.ADMIN_1[0]['password'])

    admin2 = Admin(ADMINS.ADMIN_2[0]['name'],
                   ADMINS.ADMIN_2[0]['family'],
                   ADMINS.ADMIN_2[0]['email'],
                   ADMINS.ADMIN_2[0]['password'])

    admin1.init_neo4j()
    admin2.init_neo4j()


@app.route('/')
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        return redirect(url_for("auth.login"))
    user = User.find_by_id(user_id)
    if user:
        return user
