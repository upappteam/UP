from flask import render_template, redirect, url_for

from src import create_app, login_manager
from src.users.models import User


app = create_app('develop')


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
