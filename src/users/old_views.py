from flask import Blueprint, request, render_template, flash, redirect, url_for, session

# from src.users.models import User
from src.users.models import User
from src.users.utils import Utils
from src.users.forms import RegisterForm, LoginForm, ProfileForm, ChangePasswordForm


bp_user = Blueprint('users', __name__)


@bp_user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    form_profile = ProfileForm()

    if request.method == 'POST':
        phone_number = form.phone_number.data
        password = form.password.data
        password_c = form.password_c.data
        upline_phone_number = form.upline_phone_number.data
        if not password == password_c:
            flash("The confirm password not matched.")
            return render_template('user/register.html', form=form)

        new_user = User(phone_number)
        if new_user.register(password, upline_phone_number):
            flash('Registration successful.')
            user_data = new_user.find_by_phone_number(new_user.phone_number)
            # if user of the upline phone number exist make a relationship between them
            if new_user.find_upline(upline_phone_number):
                new_user.connect_to_upline()
                # if new_user["email"]:
                #     session["email"] = new_user["email"]
                # else:
                session["phone_number"] = new_user.phone_number

                return render_template('user/profile.html', loged_in=True,
                                       user_id=user_data["_id"], form=form_profile)

            return render_template('user/profile.html', loged_in=True,
                                   user_id=user_data["_id"], form=form_profile)

        else:
            return render_template('user/register.html', form=form)

    return render_template('user/register.html', form=form)


@bp_user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        phone_number = form.phone_number.data
        password = form.password.data

        user_obj = User(phone_number)

        if user_obj:
            if user_obj.verify_password(password):
                flash("Log in successful.")
                # if user["email"]:
                #     session["email"] = user["email"]
                # else:
                user_data = User.find_by_phone_number(user_obj.phone_number)
                session["phone_number"] = user_data["phone_number"]
                print(user_data["_id"])
                # return render_template("user/home.html", loged_in=True)
                return redirect(url_for('users.home', user_id=user_data["_id"]))

            else:
                flash("The password is wrong.")
                return render_template("user/login.html", form=form)

        else:
            flash("The user does not exist.")
            return redirect(url_for('users.register'))

    return render_template('user/login.html', form=form)


@bp_user.route('/profile/<string:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    form = ProfileForm()
    form_pw = ChangePasswordForm()

    if request.method == 'POST':
        user_obj = User(session["phone_number"])
        user_data = User.find_by_id(user_id)

        if form.name.data is not None:

            if user_obj.update_info(name=form.name.data, family_name=form.family_name.data,
                                    email=form.email.data, birthday=form.birthday_day.data,
                                    company=form.company.data, gender=form.gender.data, bio=form.bio.data):
                flash("Profile view updated.")
                return redirect(url_for('users.profile', user_id=user_data["_id"]))

        else:
            return redirect(url_for('users.profile', user_id=user_data["_id"]))

    return render_template("user/profile.html", form=form, form_pw=form_pw)


@bp_user.route('/home/<string:user_id>')
def home(user_id):
    user_obj = User(session["phone_number"])
    user_data = user_obj.find_by_id(user_id)
    return render_template("user/home.html", user_id=user_data["_id"])


@bp_user.route('/change_password', methods=['GET', 'POST'])
def change_pw():
    form_pw = ChangePasswordForm()
    if request.method == 'POST':

        user_obj = User(session["phone_number"])
        # user_data = user_obj.find_by_id(session["phone_number"])

        if form_pw.current_password.data is not None and form_pw.new_password.data is not None:

            if user_obj.verify_password(form_pw.current_password.data):

                if form_pw.new_password.data == form_pw.confirm_password.data:

                    user_obj.change_password(form_pw.new_password.data)
                    flash("Your password changed.")

                    return redirect(url_for('users.change_pw'))

                else:
                    flash("Confirm password does not matched.")
                    return redirect(url_for('users.change_pw'))

            else:
                flash('Your current password is wrong.')
                return redirect(url_for('users.change_pw'))

    return render_template('user/change_pw.html', form_pw=form_pw)
