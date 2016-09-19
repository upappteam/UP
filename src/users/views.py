from flask import request, render_template, flash, redirect, url_for, session
from flask_login import current_user, login_required

from . import bp_user
from src.users.models import User
from src.users.utils import Utils
from src.users.forms import ProfileForm, ChangePasswordForm


@bp_user.route('/info/<string:user_id>', methods=['GET', 'POST'])
@login_required
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

            # if user.account_time == 'None':
            #     return redirect(url_for('payments.new_account', user_id=user._id))

            session["email"] = email

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
@login_required
def home(user_id):
    user = User.find_by_id(user_id)
    sub = User.find_sub(user_id)
    up = user.find_uplines()
    if not isinstance(sub, set) and not isinstance(up, list):
        return render_template('user/home.html', user_id=user._id,
                               name=user.name, count_sub=0, count_up=0)

    elif len(up) < 1 and len(sub) > 0:
        return render_template('user/home.html', user_id=user._id,
                               name=user.name, count_sub=len(sub), sub=sub, count_up=0)

    elif len(sub) < 1 and len(up) > 0:
        return render_template('user/home.html', user_id=user._id,
                               name=user.name, count_sub=0, up=up, count_up=len(up))

    return render_template('user/home.html', user_id=user._id,
                           name=user.name, count_sub=len(sub), sub=sub,
                           count_up=len(up), up=up)


@bp_user.route('/change_password/<string:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    user = User.find_by_id(user_id)
    form = ChangePasswordForm()
    if request.method == 'POST':
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        if Utils.check_password(user.password, current_password):
            if new_password == confirm_password:
                user.change_password(new_password)
                flash("Your password changed.")
                return redirect(url_for('users.home', user_id=user._id))

            else:
                flash("The confirm password not matched.")
                return redirect(url_for('users.change_password', user_id=user._id))

        else:
            flash("your current password is wrong.")
            return redirect(url_for('users.change_password', user_id=user._id))

    return render_template('user/change_pw.html', form=form)


@bp_user.route('/uplines/<string:user_id>')
@login_required
def view_uplines(user_id):
    user = User.find_by_id(user_id)
    up = user.find_uplines()
    if isinstance(up, list) and len(up) > 0:
        return render_template("user/view_uplines.html", up=up, count=len(up))

    return redirect(url_for('users.home', user_id=user_id, name=user.name))
