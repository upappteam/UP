# -*- coding: utf-8 -*-
from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_required, login_user

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

            if User.find_by_email(email):
                flash("This someone email address registered.")
                return redirect(url_for('users.info', user_id=current_user._id))

            login_user(user)
            user.profile(name, family, gender, company, email, birthday)

            # if user.account_time == 'None':
            #     return redirect(url_for('payments.new_account', user_id=user._id))

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


@bp_user.route('/home/<string:user_id>', methods=['GET', 'POST'])
@login_required
def home(user_id):
    user = User.find_by_id(user_id)

    if request.method == 'POST' and request.form["search"]:
        word = request.form["search"]
        return redirect(url_for('users.search', word=word))

    return render_template('user/home.html', user_id=user._id, name=user.name)


@bp_user.route('/change_password/<string:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    user = User.find_by_id(user_id)
    form = ChangePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
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
    up = user.find_uplines(user_id)
    if isinstance(up, list) and len(up) > 0:
        return render_template("user/view_uplines.html", up=up, count=len(up))

    flash("You have not any Uplines.")
    return redirect(url_for('users.home', user_id=user_id, name=user.name))


@bp_user.route('/subsets/<string:user_id>')
@login_required
def view_subsets(user_id):
    user = User.find_by_id(user_id)
    sub = User.find_sub(user_id)
    if isinstance(sub, list) and len(sub) > 0:
        return render_template("user/view_subsets.html", sub=sub, count=len(sub))
    flash("You have not any subsets yet!")
    return redirect(url_for('users.home', user_id=user_id, name=user.name))


@bp_user.route('/search/<string:word>')
@login_required
def search(word):
    word = word.strip()
    print(word)
    if "@" in word:
        flash("Can not find any user by email address.")
        return redirect(url_for('users.home', user_id=current_user._id))
    elif " " in word:
        name_family = word.split(" ")
        if len(name_family) == 2:
            name, family = name_family
            users = User.search_by_name_family(name=name, family=family)
            return render_template("user/result.html", users=users, user_id=current_user._id)
        elif len(name_family) == 3:
            name, mid_name, family = name_family
            users1 = User.search_by_name_family(name=name+mid_name, family=family)
            users2 = User.search_by_name_family(name=name, family=mid_name+family)
            users = users1 + users2
            return render_template("user/result.html", users=users, user_id=current_user._id)
    elif " " not in word:
        users = User.search_by_name_family(name=word, family=word)
        return render_template("user/result.html", users=users, user_id=current_user._id)

    flash("Could not find any user {}".format(word))
    return redirect(url_for('users.home', user_id=current_user._id))
