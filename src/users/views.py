from flask import Blueprint, request, render_template, flash, redirect, url_for

from src.users.models import User
from src.users.forms import RegisterForm, LoginForm


bp_user = Blueprint('users', __name__)


@bp_user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        phone_number = form.phone_number.data
        password = form.password.data
        password_c = form.password_c.data
        upline_phone_number = form.upline_phone_number.data
        if not password == password_c:
            # flash("The confirm password not matched.")
            return render_template('user/register.html', form=form)

        new_user = User(phone_number)
        if new_user.register(password, upline_phone_number):
            # flash('Registration successful.')

            # if user of the upline phone number exist make a relationship between them
            if new_user.find_upline(upline_phone_number):
                new_user.connect_to_upline()
            return render_template('user/home.html', loged_in=True)

        else:
            return render_template('user/register.html', form=form)

    return render_template('user/register.html', form=form)


@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        phone_number = form.phone_number.data
        password = form.password.data

        user = User(phone_number)
        if user:
            if user.verify_password(password):
                # flash("Log in success.")
                return render_template("user/home.html", loged_in=True)

            else:
                # flash("The password is wrong.")
                return render_template("user/login.html", form=form)

        else:
            # flash("The user does not exist.")
            return redirect(url_for('users.register'))

    return render_template('user/login.html', form=form)
