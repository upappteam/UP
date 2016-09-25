from flask import render_template, redirect, flash, url_for, request

from . import bp_admin
from src.users.models import User
from src.admin.models import Admin


@bp_admin.route('/home/<string:admin_id>')
def admin_home(admin_id):
    admin = Admin.classify(Admin.find_admin_id(admin_id))
    return render_template('admin/home.html', admin_id=admin._id)


@bp_admin.route('/users/<string:admin_id>', methods=['GET', 'POST'])
def admin_users(admin_id):
    search = True
    msg = None
    if request.method == 'POST':
        word = request.form["search"].strip().lower()
        if word.isdigit():
            users = []
            user = User.find_one(word)
            if user:
                user = User.classify1(user)
                users.append(user)
                return render_template("admin/users.html", admin_id=admin_id, users=users,
                                       search=search, msg=msg, activate="active")
            else:
                msg = "Not found any user by {0}".format(word)
                return render_template("admin/users.html", admin_id=admin_id,
                                       search=search, msg=msg, activate="active")

        elif word.isalpha() and '@' not in word:
            if " " in word:
                name_family = word.split(" ")
                if len(name_family) == 2:
                    name, family = name_family
                    users = User.search_by_name_family(name=name, family=family)
                    if users:
                        return render_template("admin/users.html", admin_id=admin_id, users=users,
                                               search=search, msg=msg, activate="active")
                    else:
                        msg = "Not found any user by {0}".format(word)
                        return render_template("admin/users.html", admin_id=admin_id,
                                               search=search, msg=msg, activate="active")

                elif len(name_family) == 3:
                    name, mid_name, family = name_family
                    users1 = User.search_by_name_family(name=name + " " + mid_name, family=family)
                    users2 = User.search_by_name_family(name=name, family=mid_name + " " + family)
                    users = users1 + users2
                    if users:
                        return render_template("admin/users.html", admin_id=admin_id, users=users,
                                               search=search, msg=msg, activate="active")
                    else:
                        msg = "Not found any user by {0}".format(word)
                        return render_template("admin/users.html", admin_id=admin_id,
                                               search=search, msg=msg, activate="active")

            elif " " not in word:
                users = User.search_by_name_family(name=word, family=word)
                if users:
                    return render_template("admin/users.html", admin_id=admin_id, users=users,
                                           search=search, msg=msg, activate="active")
                else:
                    msg = "Not found any user by {0}".format(word)
                    return render_template("admin/users.html", admin_id=admin_id,
                                           search=search, msg=msg, activate="active")

        elif '@' in word:
            users = []
            users.append(User.find_by_email(word))
            if users:
                return render_template("admin/users.html", admin_id=admin_id, users=users,
                                       search=search, msg=msg, activate="active")
            else:
                msg = "Not found any user by {0}".format(word)
                return render_template("admin/users.html", admin_id=admin_id,
                                       search=search, msg=msg, activate="active")

        else:
            msg = "Not found any user by {0}".format(word)
            return render_template("admin/users.html", admin_id=admin_id,
                                   search=search, msg=msg, activate="active")

    return render_template("admin/users.html", admin_id=admin_id, search=search, msg=msg, activate="active")


@bp_admin.route('/show_all_users/<string:admin_id>')
def show_all_users(admin_id):
    users = Admin.find_all_users()
    return render_template('admin/users.html', admin_id=admin_id, users=users,
                           search=False, msg=None, activate="active")


@bp_admin.route('/posts/<string:admin_id>')
def admin_posts(admin_id):
    if request.form == 'POST':
        pass
    return render_template("admin/posts.html", admin_id=admin_id)


@bp_admin.route('/posts/find_posts/<string:admin_id>')
def find_posts(admin_id):
    pass


@bp_admin.route('/posts/find_all_public/<string:admin_id>')
def find_all_public(admin_id):
    pass


@bp_admin.route('/posts/find_all_private/<string:admin_id>')
def find_all_private(admin_id):
    pass


@bp_admin.route('/posts/find_all_subsets/<string:admin_id>')
def find_all_subsets(admin_id):
    pass


@bp_admin.route('/posts/find_all_uplene/<string:admin_id>')
def find_all_uplene(admin_id):
    pass


@bp_admin.route('/posts/find_all_direct/<string:admin_id>')
def find_all_direct(admin_id):
    pass


@bp_admin.route('/messages/send/<string:admin_id>')
def admin_send_message(admin_id):
    pass


@bp_admin.route('/messages/received/<string:admin_id>')
def admin_read_message(admin_id):
    pass
