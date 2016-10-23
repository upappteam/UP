from flask import redirect,url_for
from . import bp_common
from flask_login import login_required,current_user


@bp_common.route('/home/')
@login_required
def home():
    return 'here is home'


@bp_common.route('/login/')
def login():
    return redirect(url_for('auth.login'))

