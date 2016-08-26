from flask import Blueprint, request, render_template, flash, redirect, url_for, session

from src.users.models import User
from src.users.utils import Utils
from src.users.forms import RegisterForm, LoginForm, ProfileForm, ChangePasswordForm


bp_user = Blueprint('users', __name__)


@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        phone_number = form.phone_number.data
        password = form.password.data

        user = User.find_one(phone_number)
        if user.valid_phone_number(phone_number):
            if Utils.check_password(user.password, password):
                flash("Log in successful.")
                return redirect(url_for('users.home', user_id=user._id))
            else:
                flash("Your password was wrong.")
                return redirect(url_for('login'))
        else:
            flash("The user does not exist.")
            return redirect(url_for('login'))
    return render_template('user/login.html', form=form)


@bp_user.route('/register', methods=['GET', 'POST'])
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
                                password=Utils.set_password(password),)
                new_user.register()
                return redirect(url_for('users.info', user_id=new_user._id))

        else:
            flash("User exists with this phone number.")
            return redirect(url_for('register'))

    return render_template('user/register.html', form=form)


@bp_user.route('/info/<string:user_id>')
def info(user_id):
    user = User.find_by_id(user_id)

    if user.name == 'None':
        form = ProfileForm()
        if request.method == 'POST':
            email = form.email.data
            name = form.name.data
            family = form.family_name.data
            gender = form.gender.data
            company = form.company.data
            birthday = form.birthday_day.data

            user.profile(name, family, gender, company, email, birthday)

            return redirect(url_for('users.home', user_id=user._id))

        return render_template('user/profile.html', form=form)

    else:
        form = ChangePasswordForm()

        if request.method == 'POST':
            current_password = form.current_password
            new_password = form.new_password.data
            confirm_password = form.confirm_password.data

            if Utils.check_password(user.password, current_password):
                if new_password == confirm_password:
                    user.change_password(new_password)
                    flash("Your password changed.")
                    return redirect(url_for('users.home', user_id=user._id))
                else:
                    flash("The confirm password not matched.")
                    return redirect(url_for('users.info', user_id=user._id))
            else:
                flash("Your current password is wrong.")
                return redirect(url_for('users.info', user_id=user._id))
        return render_template('user/change_pw.html', form_pw=form)


@bp_user.route('/home/<string:user_id>')
def home(user_id):
    user = User.find_by_id(user_id)
    return render_template('user/home.html', user_id=user._id, name=user.name)
