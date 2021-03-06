# -*- coding: utf-8 -*-
from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_required

from src.common.models import just_current_user
from src.users.forms import ProfileForm, ChangePasswordForm
from src.users.models import User
from src.utils.models import Utils
from . import bp_user


@bp_user.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    if current_user.name == 'none':
        form = ProfileForm()
        if request.method == 'POST':
            email = form.email.data
            name = form.name.data
            family = form.family_name.data
            gender = form.gender.data
            company = form.company.data
            birthday = form.birthday_day.data
            brtd = birthday.split('/')
            if len(brtd) is not 3:
                flash("Make sure Date Time is in correct format:\nYYYY/MM/DD")
                return redirect(url_for(url_for('users.info')))

            if User.find_by_email(email):
                flash("This someone email address registered.")
                return redirect(url_for('users.info'))

            birthday = "-".join(brtd)
            current_user.profile(name, family, gender, company, email, birthday)

            # if user.account_time == 'None':
            #     return redirect(url_for('payments.new_account', user_id=user._id))

            return redirect(url_for('users.home'))

        return render_template('user/profile.html', form=form)

    return redirect(url_for('users.view_profile'))
    # else:
    #     form = ChangePasswordForm()
    #
    #     if request.method == 'POST':
    #         current_password = form.current_password
    #         new_password = form.new_password.data
    #         confirm_password = form.confirm_password.data
    #
    #         if Utils.check_password(user.password, current_password):
    #             if new_password == confirm_password:
    #                 user.change_password(new_password)
    #                 flash("Your password changed.")
    #                 return redirect(url_for('users.home', user_id=user._id))
    #             else:
    #                 flash("The confirm password not matched.")
    #                 return redirect(url_for('users.info', user_id=user._id))
    #         else:
    #             flash("Your current password is wrong.")
    #             return redirect(url_for('users.info', user_id=user._id))
    #     return render_template('user/change_pw.html', form_pw=form)


@bp_user.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST' and request.form["search"]:
        word = request.form["search"]
        return redirect(url_for('users.search', word=word))

    return render_template('user/home.html', current=current_user)


# TODO Change password by TOKEN not this
@bp_user.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        if Utils.check_password(current_user.password, current_password):
            if new_password == confirm_password:
                current_user.change_password(new_password)
                flash("Your password changed.")
                return redirect(url_for('users.home'))

            else:
                flash("The confirm password not matched.")
                return redirect(url_for('users.change_password'))

        else:
            flash("your current password is wrong.")
            return redirect(url_for('users.change_password'))

    return render_template('user/change_pw.html', form=form)


# TODO Make sure to work this route
@bp_user.route('/uplines')
@login_required
def view_uplines():
    up = current_user.find_uplines(current_user._id)
    if isinstance(up, list) and len(up) > 0:
        return render_template("user/view_uplines.html", up=up, count=len(up))

    flash("You have not any Uplines.")
    return redirect(url_for('users.home', name=current_user.name))


# TODO Make sure to work this route
@bp_user.route('/subsets')
@login_required
def view_subsets():
    sub = User.find_sub(current_user._id)
    if isinstance(sub, list) and len(sub) > 0:
        return render_template("user/view_subsets.html", sub=sub, count=len(sub))
    flash("You have not any subsets yet!")
    return redirect(url_for('users.home', name=current_user.name))


@bp_user.route('/search/<string:word>')
@login_required
def search(word):
    word_ = word.strip()
    if "@" in word_:
        flash("Can not find any user by email address.")
        return redirect(url_for('users.home'))
    elif " " in word_:
        name_family = word_.split(" ")
        if len(name_family) == 2:
            name, family = name_family
            users = User.search_by_name_family(name=name, family=family)
            return render_template("user/result.html", users=users)
        elif len(name_family) == 3:
            name, mid_name, family = name_family
            users1 = User.search_by_name_family(name=name+mid_name, family=family)
            users2 = User.search_by_name_family(name=name, family=mid_name+family)
            users = users1 + users2
            return render_template("user/result.html", users=users)
    elif " " not in word_:
        users = User.search_by_name_family(name=word_, family=word_)
        return render_template("user/result.html", users=users)

    flash("Could not find any user {}".format(word_))
    return redirect(url_for('users.home'))


# TODO Find new way to do this (WITHOUT SENDING USER_ID)
@bp_user.route('/profile/view/<string:user_id>')
@login_required
def view_profile(user_id):
    user = User.find_by_id(user_id)
    if not User.check_follow_relation(current_user._id, user_id):
        request.form.follow = "Follow"
    else:
        request.form.follow = "Un Follow"
    return render_template("user/personal_page.html", user=user)


# TODO Find new way to do this (WITHOUT SENDING USER_ID)
@bp_user.route('/profile/edit')
@login_required
def edit_profile():
    # TODO Make edit page
    return render_template("user/personal_page.html")


# TODO Find new way to do this (WITHOUT SENDING USER_EMAIL)
@bp_user.route('/find_user_by_email/<string:user_email>')
@login_required
def find_user_by_email_and_redirect(user_email):
    user = User.classify1(User.find_by_email(user_email))
    return redirect(url_for('users.view_profile', user_id=user._id))


# TODO Find new way to do this (WITHOUT SENDING USER_ID)
@bp_user.route('/follow/<string:user_id>')
@login_required
@just_current_user
def follow(user_id):
    if not User.check_follow_relation(current_user._id, user_id):
        User.follow_user(current_user._id, user_id)
    elif User.check_follow_relation(current_user._id, user_id):
        User.un_follow_user(current_user._id, user_id)
    return redirect(url_for('users.view_profile', user_id=user_id))


# TODO Find new way to do this (WITHOUT SENDING USER_ID)
@bp_user.route('/home1/<string:user_id>')
@login_required
@just_current_user
def follow1(user_id):
    return str(request.referrer)


# TODO Find new way to do this (WITHOUT SENDING USER_ID)
@bp_user.route('/home2/<string:user_id>')
@login_required
@just_current_user
def follow2(user_id):
    return redirect(url_for('users.follow1', user_id=user_id))


@bp_user.route('/feedback')
@login_required
def feedback():
    return render_template("post/feedback.html")
