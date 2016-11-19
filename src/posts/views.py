from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from . import bp_post
from src.users.models import User
from src.posts.models import Post
from src.posts.forms import PostForm, EditForm


# TODO Read posts by type publication
# TODO Write posts by type publication
# TODO Comment in every posts
# TODO List of subsets

@bp_post.route('/sent')
@login_required
def view_sent_posts():
    """
    View all posts sent by this user.
    Of course not messages.
    :param user_id: _id of user to find the user.
    :return: A page with all posts sent by this user.
    """
    posts = Post.find_all_by_email(current_user.email)
    if posts:
        posts_length = len(posts)
    else:
        posts_length = 0
    return render_template('post/view_posts.html', posts=posts, posts_length=posts_length)


@bp_post.route('/new', methods=['GET', 'POST'])
@login_required
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
        user_data = User.find_by_email(current_user.email)

        if type_publication == 'public':
            Post(user_data["email"], subject, content, type_publication=type_publication).insert(_type=type_publication)

        elif type_publication == 'uplines':
            uplines = current_user.find_uplines(current_user._id)
            if uplines:
                post = Post(user_data["email"], subject, content,type_publication=type_publication)
                post.insert(type_publication)
                for up in uplines:
                    Post.connect(up.email, post._id, type_publication)
            else:
                flash("You have not any uplines.")
                return redirect(url_for('posts.new_post'))

        elif type_publication == 'subsets':
            subsets = User.find_sub(current_user._id)
            if subsets:
                post = Post(user_data["email"], subject, content, type_publication=type_publication)
                post.insert(type_publication)
                for sub in subsets:
                    Post.connect(sub.email, post._id, type_publication)
            else:
                flash("You have not any subsets.")
                return redirect(url_for('posts.new_post'))

        elif type_publication == 'directs':
            directs = User.find_directs(current_user.email)
            if directs:
                post = Post(user_data["email"], subject, content, type_publication=type_publication)
                post.insert(type_publication)
                for direct in directs:
                    Post.connect(direct.email, post._id, type_publication)
            else:
                flash("You have not any directs.")
                return redirect(url_for('posts.new_post'))

        elif type_publication == 'upline':
            upline = User.find_one(current_user.upline_phone_number)
            if upline:
                post = Post(user_data["email"], subject, content, type_publication=type_publication)
                post.insert(type_publication)
                Post.connect(upline["email"], post._id, type_publication)

            else:
                flash("You have not any upline.")
                return redirect(url_for('posts.new_post'))

        return redirect(url_for('posts.view_sent_posts'))

    return render_template("post/new_post.html", form=form)


@bp_post.route('/edit/<string:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """
    Edit sent post.
    :param post_id: _id of the post for edit that.
    :return: Edited post.
    """
    form = EditForm()
    post = Post.find_one(post_id)

    if request.method == 'POST':
        subject = form.subject.data
        content = form.content.data

        if subject is not None and content is not None:
            Post.edit(post_id, subject, content)
            flash("Post edited.")
            return redirect(url_for('posts.view_sent_posts', post=post))

        flash("fields can not be empty.")
        return redirect(url_for('posts.edit_post', post_id=post_id))

    form.subject.data = post["subject"]
    form.content.data = post["content"]
    return render_template('post/edit.html', form=form)


@bp_post.route('/delete/<string:post_id>')
@login_required
def delete_post(post_id):
    """
    Delete post.
    :param post_id: _id post for delete that.
    :return: Redirect to view sent posts page.
    """
    user = User.find_by_email(current_user.email)
    Post.delete(post_id, user)
    flash("Post deleted.")
    return redirect(url_for('posts.view_sent_posts'))


@bp_post.route('/public')
@login_required
def view_public_posts():
    """
    View all public post sent by everyone.
    :return: A page of all public posts.
    """
    posts = Post.find_all_public(current_user._id)
    message = "There is no public posts."
    return render_template('post/public_posts.html',
                           posts=posts,
                           title='Public posts', msg=message, user_email=current_user.email)


@bp_post.route('/from_subsets')
@login_required
def posts_from_subsets():
    posts = Post.find_message_by_type(current_user.email, 'uplines')
    message = "There is no posts from subsets."
    return render_template("post/public_posts.html",
                           posts=posts,
                           title='Posts from subsets', msg=message)


@bp_post.route('/from_uplines')
@login_required
def posts_from_uplines():
    posts = Post.find_message_by_type(current_user.email, 'subsets')
    message = "There is no posts from uplines."
    return render_template("post/public_posts.html",
                           posts=posts,
                           title='Posts from uplines', msg=message)


@bp_post.route('/for_directs')
@login_required
def posts_for_directs():
    posts = Post.find_message_by_type(current_user.email, 'directs')
    message = "There is no posts for directs."
    return render_template("post/public_posts.html",
                           posts=posts,
                           title='Posts for directs', msg=message)
