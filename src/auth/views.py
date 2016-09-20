from flask_login import current_user, login_required, login_user, logout_user
from flask import request, redirect, url_for, flash, render_template

from . import bp_auth
from src.users.models import User
from src.users.utils import Utils
from src.auth.forms import RegisterForm, LoginForm


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        phone_number = form.phone_number.data
        password = form.password.data
        remember_me = form.remember_me.data

        user_data = User.find_one(phone_number)
        if not user_data:
            return redirect(url_for('auth.register'))
        user = User.classify1(user_data)
        # check user account time
        # if user.account_time == 'None':
        #     return redirect(url_for('payments.new_account', user_id=user._id))

        # elif user.account_time

        if user.valid_phone_number(phone_number):
            if Utils.check_password(user.password, password):
                flash("Log in successful.")
                login_user(user, remember_me)
                return redirect(url_for('users.home', user_id=user._id))
            else:
                flash("Your password was wrong.")
                return redirect(url_for('auth.login'))
        else:
            flash("The user does not exist.")
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)


@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        phone_number = form.phone_number.data
        upline_phone_number = form.upline_phone_number.data
        password = form.password.data
        password_c = form.password_c.data

        if not User.valid_phone_number(phone_number):
            if User.valid_phone_number(upline_phone_number) and password == password_c:
                new_user = User(phone_number=phone_number,
                                upline_phone_number=upline_phone_number,
                                password=Utils.set_password(password))
                new_user.register()
                new_user.connect_to_upline()

                return redirect(url_for('users.info', user_id=new_user._id))

        else:
            flash("User exists with this phone number.")
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html', form=form)


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been log out.")
    return redirect(url_for('index'))