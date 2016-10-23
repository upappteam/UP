from flask import render_template, flash, request, redirect, url_for, session

from . import bp_admin
from src.users.models import User
from src.posts.models import Post
from src.admin.models import Admin


@bp_admin.route('/home/<string:admin_id>')
def admin_home(admin_id):
    posts = Post.admin_sent_posts()
    if posts:
        return render_template('admin/home.html', admin_id=admin_id, posts=posts, admin_email=session["email"])
    return render_template('admin/home.html', admin_id=admin_id, admin_email=session["email"])


@bp_admin.route('/posts_sent/edit/<string:post_id>', methods=['GET', 'POST'])
def admin_posts_edit(post_id):
    admin = Admin.find_admin_email(session["email"])
    post = Post.find_one(post_id)

    if request.method == 'POST':
        title = request.form["title"]
        content = request.form["content"]
        Post.admin_sent_posts_edit(post_id, title, content)
        return redirect(url_for('admins.admin_home', admin_id=admin["_id"]))

    request.form.title = post["subject"]
    request.form.content = post["content"]

    return render_template("admin/edit.html", admin_id=admin["_id"])


@bp_admin.route('/posts_sent/delete/<string:post_id>')
def admin_posts_delete(post_id):
    admin = Admin.find_admin_email(session["email"])
    Post.admin_sent_posts_delete(post_id)
    flash("Post DELETED")
    return redirect(url_for('admins.admin_home', admin_id=admin["_id"]))


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
                                       search=search, msg=msg, activate="active", nothing=True)

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
                                               search=search, msg=msg, activate="active", nothing=True)

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
                                               search=search, msg=msg, activate="active", nothing=True)

            elif " " not in word:
                users = User.search_by_name_family(name=word, family=word)
                if users:
                    return render_template("admin/users.html", admin_id=admin_id, users=users,
                                           search=search, msg=msg, activate="active")
                else:
                    msg = "Not found any user by {0}".format(word)
                    return render_template("admin/users.html", admin_id=admin_id,
                                           search=search, msg=msg, activate="active", nothing=True)

        elif '@' in word:
            users = []
            users.append(User.find_by_email(word))
            if users:
                return render_template("admin/users.html", admin_id=admin_id, users=users,
                                       search=search, msg=msg, activate="active")
            else:
                msg = "Not found any user by {0}".format(word)
                return render_template("admin/users.html", admin_id=admin_id,
                                       search=search, msg=msg, activate="active", nothing=True)

        else:
            msg = "Not found any user by {0}".format(word)
            return render_template("admin/users.html", admin_id=admin_id,
                                   search=search, msg=msg, activate="active", nothing=True)

    return render_template("admin/users.html", admin_id=admin_id, search=search, msg=msg, activate="active", nothing=True)


@bp_admin.route('/show_all_users/<string:admin_id>')
def show_all_users(admin_id):
    users = Admin.find_all_users()
    return render_template('admin/users.html', admin_id=admin_id, users=users,
                           search=False, msg=None, activate="active")


@bp_admin.route('/posts/<string:admin_id>', methods=['GET', 'POST'])
def admin_posts(admin_id):
    search = True
    msg = None
    if request.method == 'POST':
        if request.form["search"]:
            word = request.form["search"].strip()
            option = request.form["radio"]

            if option == 'author':
                user = User.find_by_email(word)
                if not user:
                    msg = "There is no user by this email: {0}".format(word)
                    return render_template("admin/posts.html", admin_id=admin_id, activate='active', search=search, msg=msg)
                posts = Post.admin_find_posts_by_author(word)
                if posts:
                    search = None
                    return render_template("admin/posts.html",
                                           admin_id=admin_id,
                                           activate='active',
                                           search=search,
                                           msg=msg,
                                           posts=posts)
                else:
                    msg = "There is no post by this author: {0}".format(word)
                    return render_template("admin/posts.html", admin_id=admin_id, activate='active', search=search, msg=msg)

            elif option == 'date':
                if '-' in word:
                    date = word.split('-')
                    if len(date) >= 2:
                        posts = Post.admin_find_posts_by_date(*date)
                        search = None
                        return render_template("admin/posts.html",
                                               admin_id=admin_id,
                                               activate='active',
                                               search=search,
                                               msg=msg,
                                               posts=posts)
                elif word.isdigit():
                    date = [word]
                    posts = Post.admin_find_posts_by_date(*date)
                    search = None
                    return render_template("admin/posts.html",
                                           admin_id=admin_id,
                                           activate='active',
                                           search=search,
                                           msg=msg,
                                           posts=posts)

                else:
                    msg = "There is no post in this date: {0}\n Date format should be YEAR-MONTH-DAY-HOUR".format(word)
                    return render_template("admin/posts.html", admin_id=admin_id, activate='active', search=search, msg=msg)

            elif option == 'title':
                if ' ' in word:
                    word = word.split(' ')
                    posts = Post.admin_find_posts_by_title(*word)
                    if posts:
                        search = None
                        return render_template("admin/posts.html",
                                               admin_id=admin_id,
                                               activate='active',
                                               search=search,
                                               msg=msg,
                                               posts=posts)

                    else:
                        msg = "There is no post by this title: {0}".format(word)
                        return render_template("admin/posts.html", admin_id=admin_id, activate='active', search=search, msg=msg)

                elif ' ' not in word:
                    word = [word]
                    posts = Post.admin_find_posts_by_title(*word)
                    if posts:
                        search = None
                        return render_template("admin/posts.html",
                                               admin_id=admin_id,
                                               activate='active',
                                               search=search,
                                               msg=msg,
                                               posts=posts)

                    else:
                        msg = "There is no post by this title: {0}".format(word)
                        return render_template("admin/posts.html", admin_id=admin_id, activate='active', search=search, msg=msg)

            elif option == 'content':
                if ' ' in word:
                    words = word.split(' ')
                    posts = Post.admin_find_posts_by_content(*words)
                    if posts:
                        search = None
                        return render_template("admin/posts.html",
                                               admin_id=admin_id,
                                               activate='active',
                                               search=search,
                                               msg=msg,
                                               posts=posts)

                    else:
                        msg = "There is no post by this content: {0}".format(word)
                        return render_template("admin/posts.html", admin_id=admin_id, activate='active', search=search, msg=msg)

                elif ' ' not in word:
                    word = [word]
                    posts = Post.admin_find_posts_by_content(*word)
                    if posts:
                        search = None
                        return render_template("admin/posts.html",
                                               admin_id=admin_id,
                                               activate='active',
                                               search=search,
                                               msg=msg,
                                               posts=posts)

                    else:
                        msg = "There is no post by this content: {0}".format(word)
                        return render_template("admin/posts.html", admin_id=admin_id, activate='active', search=search, msg=msg)

        else:
            msg = "Enter an email or title or date or a word of content."

    return render_template("admin/posts.html", admin_id=admin_id, activate='active', search=search, msg=msg)


@bp_admin.route('/posts/find_posts/<string:admin_id>')
def find_posts(admin_id):
    posts = Post.admin_find_all_posts()
    search = None
    msg = None
    return render_template('admin/posts.html', admin_id=admin_id, activate='active', search=search, posts=posts, msg=msg)


@bp_admin.route('/posts/find_all_public/<string:admin_id>')
def find_all_public(admin_id):
    posts = Post.admin_find_all_posts_by_type('public')
    search = None
    msg = None
    return render_template('admin/posts.html', admin_id=admin_id, activate='active', search=search, posts=posts, msg=msg)


@bp_admin.route('/posts/find_all_private/<string:admin_id>')
def find_all_private(admin_id):
    posts = Post.admin_find_all_posts_by_type('private')
    search = None
    msg = None
    return render_template('admin/posts.html', admin_id=admin_id, activate='active', search=search, posts=posts, msg=msg)


@bp_admin.route('/posts/find_all_subsets/<string:admin_id>')
def find_all_subsets(admin_id):
    posts = Post.admin_find_all_posts_by_type('subsets')
    search = None
    msg = None
    return render_template('admin/posts.html', admin_id=admin_id, activate='active', search=search, posts=posts, msg=msg)


@bp_admin.route('/posts/find_all_uplene/<string:admin_id>')
def find_all_uplines(admin_id):
    posts = Post.admin_find_all_posts_by_type('uplines')
    search = None
    msg = None
    return render_template('admin/posts.html', admin_id=admin_id, activate='active', search=search, posts=posts, msg=msg)


@bp_admin.route('/posts/find_all_upline/<string:admin_id>')
def find_all_upline(admin_id):
    posts = Post.admin_find_all_posts_by_type('upline')
    search = None
    msg = None
    return render_template('admin/posts.html', admin_id=admin_id, activate='active', search=search, posts=posts, msg=msg)


@bp_admin.route('/posts/find_all_direct/<string:admin_id>')
def find_all_direct(admin_id):
    posts = Post.admin_find_all_posts_by_type('directs')
    search = None
    msg = None
    return render_template('admin/posts.html', admin_id=admin_id, activate='active', search=search, posts=posts, msg=msg)


@bp_admin.route('/messages/send/<string:admin_id>', methods=['GET', 'POST'])
def admin_send_message(admin_id):
    if request.method == 'POST':
        mode = request.form["radio"]
        admin = Admin.find_admin_id(admin_id)

        if mode == 'one':
            email = request.form["user_email"]
            user = User.find_by_email(email)
            if user:
                subject = request.form["title"]
                content = request.form["content"]
                Post("admin", subject, content).admin_insert_post_by_type(admin, email, 'private')
                posts = Post.admin_sent_posts()
                flash("Message sent to {0}".format(email))
                return render_template("admin/home.html", admin_id=admin_id, posts=posts)
            else:
                flash("The user you choose by {} does not exist.".format(email))
                return render_template("admin/send_message.html", admin_id=admin_id)
        elif mode == 'all':
            subject = request.form["title"]
            content = request.form["content"]
            users = User.admin_find_all_users()
            new_post = Post("admin", subject, content)
            new_post.admin_insert_post(admin, 'private')
            for user in users:
                Post.connect(user.email, new_post._id, 'private')
            posts = Post.admin_sent_posts()
            flash("Post sent to all.")
            return render_template("admin/home.html", admin_id=admin_id, posts=posts)
    return render_template("admin/send_message.html", admin_id=admin_id)


@bp_admin.route('/messages/received/<string:admin_id>')
def admin_read_message(admin_id):
    posts = Post.admin_read_messages()
    return render_template("admin/read_message.html", admin_id=admin_id, posts=posts)
