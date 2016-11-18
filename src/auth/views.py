from flask_login import login_required, login_user, logout_user, current_user
from flask import redirect, url_for, flash, render_template, session, g, current_app, appcontext_pushed

from . import bp_auth
from src.admin.models import Admin
from src.users.models import User
from src.users.utils import Utils
from src.auth.forms import RegisterForm, LoginForm


@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('users.home', user_id=current_user._id))
    form = LoginForm()
    if form.validate_on_submit():
        phone_number = form.phone_number.data
        password = form.password.data
        remember_me = form.remember_me.data

        if '@' in phone_number and phone_number == Admin.find_admin_email(phone_number)["email"]:
            admin_data = Admin.find_admin_email(phone_number)
            if admin_data:
                admin = Admin.classify(name=admin_data["name"],
                                       family=admin_data["family"],
                                       email=admin_data["email"],
                                       password=admin_data["password"],
                                       permission=admin_data["permission"],
                                       _id=admin_data["_id"])
                if admin.check_pw(password):
                    session["email"] = admin.email
                    login_user(user=admin, remember=remember_me)

                    return redirect(url_for('admins.admin_home'))

        user_data = User.find_one(phone_number)
        if not user_data:
            flash('User does not exists.')
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
                if user.name == 'none':
                    return redirect(url_for("users.info", user_id=user._id))
                else:
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

    if current_user.is_authenticated is True:
        flash('You are registerd before!')
        return redirect(url_for('users.home', user_id=current_user._id))

    form = RegisterForm()
    if form.validate_on_submit():

        phone_number = form.phone_number.data
        upline_phone_number = 'None' if form.work_alone.data is True else form.upline_phone_number.data
        password = form.password.data
        password_c = form.password_c.data

        if not User.valid_phone_number(phone_number):

            if form.work_alone.data is False:

                if User.valid_phone_number(upline_phone_number) and password == password_c:
                    new_user = User(phone_number=phone_number,
                                    upline_phone_number=upline_phone_number,
                                    password=Utils.set_password(password))
                    new_user.register()
                    login_user(new_user)
                    new_user.connect_to_upline()

                    return redirect(url_for('users.info', user_id=new_user._id))

                else:
                    flash("Check the fields upline phone number or password confirm not matched.")
                    return redirect(url_for('auth.register'))

            elif form.work_alone.data is True and upline_phone_number is 'None':
                if password == password_c:
                    new_user = User(phone_number=phone_number,
                                    upline_phone_number=upline_phone_number,
                                    password=Utils.set_password(password))
                    new_user.register()
                    login_user(new_user)

                    return redirect(url_for('users.info', user_id=new_user._id))

        else:
            flash("User exists with this phone number.")
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html', form=form)


@bp_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been log out.", "alert-info")
    return redirect(url_for('index'))
