from flask import Blueprint, request, render_template, flash, redirect, url_for
from src.users.forms import RegisterForm

from src.users.models import User


bp_user = Blueprint('users', __name__)


@bp_user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        phone_number = form.phone_number.data
        password = form.password.data
        upline_phone_number = form.upline_phone_number.data

        new_user = User(phone_number)
        if new_user.register(password, upline_phone_number):
            # flash('Registration successful.')

            return redirect(url_for('index'))

        else:
            return render_template('user/register.html', form=form)

    return render_template('user/register.html', form=form)
