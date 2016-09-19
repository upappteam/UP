from flask import redirect, request, session, url_for, flash, render_template
from flask_login import login_required

from . import bp_message
from src.posts.models import Post
from src.users.models import User
from src.messages.forms import NewMessage


@bp_message.route('/new', methods=['GET', 'POST'])
@login_required
def new_post_pv():
    form = NewMessage()
    if request.method == 'POST':
        subject = form.subject.data
        to = form.to.data
        content = form.content.data

        if to.isalnum():
            user = User.find_one(to)
            user_email = user["email"]
        else:
            user = User.find_by_email(to)
            user_email = user["email"]

        if user_email:
            Post(user_email=session["email"],
                 subject=subject,
                 content=content,
                 type_publication="private").insert_by_type(to=user_email,
                                                            user_email=user_email,
                                                            _type='private')

            user = User.find_by_email(session["email"])
            flash("Message sent to {0}".format(to))
            return redirect(url_for('messages.inbox', user_id=user["_id"]))

        flash("There is no user with this email or phone number.")
        return redirect(url_for('messages.new_post_pv'))

    return render_template("message/new_pv.html", form=form)


@bp_message.route('/replay/<string:author>', methods=['GET', 'POST'])
@login_required
def replay(author):
    form = NewMessage()
    if request.method == 'POST':
        subject = form.subject.data
        content = form.content.data
        to = form.to.data

        if to.isalnum():
            user = User.find_one(to)
            user_email = user["email"]
        else:
            user = User.find_by_email(to)
            user_email = user["email"]

        if user and user_email != session["email"]:
            Post(user_email=session["email"],
                 subject=subject,
                 content=content,
                 type_publication="private").insert_by_type(to=user_email, user_email=user_email)

            user = User.find_by_email(session["email"])
            flash("Message sent to {0}".format(to))
            return redirect(url_for('posts.inbox', user_id=user["_id"]))

        else:
            flash("Wrong user.")
            return redirect(url_for('messages.inbox', user_id=user["_id"]))

    form.to.data = author
    return render_template("message/new_pv.html", form=form)


@bp_message.route('/inbox/<string:user_id>')
@login_required
def inbox(user_id):
    user = User.find_by_id(user_id)
    posts = Post.find_message(user.email)

    return render_template("message/inbox.html", posts=posts)


@bp_message.route('/inbox/delete/<string:post_id>')
@login_required
def delete_message_inbox(post_id):
    user = User.find_by_email(session["email"])
    if Post.delete_message_inbox(post_id, user):
        flash("Message deleted.")
    return redirect(url_for('messages.inbox', user_id=user["_id"]))


@bp_message.route('/outbox/delete/<string:post_id>')
@login_required
def delete_message_outbox(post_id):
    user = User.find_by_email(session["email"])
    if Post.delete_message_inbox(post_id, user):
        flash("Message deleted.")
    return redirect(url_for('messages.outbox', user_id=user["_id"]))


@bp_message.route('/outbox/<string:user_id>')
def outbox(user_id):
    user_data = User.find_by_id(user_id)
    posts = Post.find_all_type(user_data.email, 'private')
    if posts:
        posts_length = len(posts)
    else:
        posts_length = 0
    return render_template('message/outbox.html', posts=posts,
                           user_id=user_data._id, posts_length=posts_length)
