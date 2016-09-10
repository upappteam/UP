from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from src.users.models import User
from src.posts.models import Post
from src.posts.forms import PostForm, EditForm


bp_post = Blueprint('posts', __name__)


@bp_post.route('/<string:user_id>')
def view_posts(user_id):
    user_data = User.find_by_id(user_id)
    posts = Post.find_all_by_email(user_data.email)
    return render_template('post/view_posts.html', posts=posts, user_id=user_data._id)


@bp_post.route('/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if request.method == 'POST':
        subject = form.subject.data
        content = form.content.data
        user_data = User.find_by_email(session["email"])
        print(user_data)
        Post(user_data["email"], subject, content).insert()
        return redirect(url_for('posts.view_posts', user_id=user_data["_id"]))

    return render_template("post/new_post.html", form=form)


@bp_post.route('/edit/<string:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    form = EditForm()

    if request.method == 'POST':
        post = Post.find_one(post_id)
        user = User.find_by_email(session["email"])
        subject = form.subject.data
        content = form.content.data

        if subject is not None and content is not None:
            Post.edit(post_id, subject, content)
            flash("Post edited.")
            return redirect(url_for('posts.view_posts', user_id=user["_id"], post=post))

        flash("fields can not be empty.")
        return redirect(url_for('posts.edit_post', post_id=post_id))

    return render_template('post/edit.html', form=form)


@bp_post.route('/delete/<string:post_id>')
def delete_post(post_id):
    user = User.find_by_email(session["email"])
    Post.delete(post_id, user)
    flash("Post deleted.")
    return redirect(url_for('posts.view_posts', user_id=user["_id"]))
