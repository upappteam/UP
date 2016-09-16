from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from src.users.models import User
from src.posts.models import Post
from src.posts.forms import PostForm, EditForm


bp_post = Blueprint('posts', __name__)


# TODO Read posts by type publication
# TODO Write posts by type publication
# TODO Comment in every posts
# TODO List of subsets

@bp_post.route('/sent/<string:user_id>')
def view_sent_posts(user_id):
    """
    View all posts sent by this user.
    Of course not messages.
    :param user_id: _id of user to find the user.
    :return: A page with all posts sent by this user.
    """
    user_data = User.find_by_id(user_id)
    posts = Post.find_all_by_email(user_data.email)
    posts_length = len(posts)
    return render_template('post/view_posts.html', posts=posts,
                           user_id=user_data._id, posts_length=posts_length)


@bp_post.route('/new', methods=['GET', 'POST'])
def new_post():
    """
    Write a new post with type publications :
    1.public
    2.subsets
    3.uplines
    4.directs
    5.upline
    :return: Data from new post page.
    """
    form = PostForm()
    if request.method == 'POST':
        subject = form.subject.data
        content = form.content.data
        type_publication = form.type_publication.data
        user_data = User.find_by_email(session["email"])

        Post(user_data["email"], subject, content, type_publication=type_publication).insert(_type=type_publication)

        return redirect(url_for('posts.view_sent_posts', user_id=user_data["_id"]))

    return render_template("post/new_post.html", form=form)


@bp_post.route('/edit/<string:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    """
    Edit sent post.
    :param post_id: _id of the post for edit that.
    :return: Edited post.
    """
    form = EditForm()
    post = Post.find_one(post_id)

    if request.method == 'POST':
        user = User.find_by_email(session["email"])
        subject = form.subject.data
        content = form.content.data

        if subject is not None and content is not None:
            Post.edit(post_id, subject, content)
            flash("Post edited.")
            return redirect(url_for('posts.view_sent_posts', user_id=user["_id"], post=post))

        flash("fields can not be empty.")
        return redirect(url_for('posts.edit_post', post_id=post_id))

    form.subject.data = post["subject"]
    form.content.data = post["content"]
    return render_template('post/edit.html', form=form)


@bp_post.route('/delete/<string:post_id>')
def delete_post(post_id):
    """
    Delete post.
    :param post_id: _id post for delete that.
    :return: Redirect to view sent posts page.
    """
    user = User.find_by_email(session["email"])
    Post.delete(post_id, user)
    flash("Post deleted.")
    return redirect(url_for('posts.view_sent_posts', user_id=user["_id"]))


@bp_post.route('/public')
def view_public_posts():
    """
    View all public post sent by everyone.
    :return: A page of all public posts.
    """
    posts = Post.find_all_public()

    return render_template('post/public_posts.html', posts=posts)
