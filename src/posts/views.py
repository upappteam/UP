from flask import render_template, request, session, redirect, url_for, flash
from flask_login import login_required

from . import bp_post
from src.users.models import User
from src.posts.models import Post
from src.posts.forms import PostForm, EditForm


# TODO Read posts by type publication
# TODO Write posts by type publication
# TODO Comment in every posts
# TODO List of subsets

@bp_post.route('/sent/<string:user_id>')
@login_required
def view_sent_posts(user_id):
    """
    View all posts sent by this user.
    Of course not messages.
    :param user_id: _id of user to find the user.
    :return: A page with all posts sent by this user.
    """
    user_data = User.find_by_id(user_id)
    posts = Post.find_all_by_email(user_data.email)
    if posts:
        posts_length = len(posts)
    else:
        posts_length = 0
    return render_template('post/view_posts.html', posts=posts,
                           user_id=user_data._id, posts_length=posts_length)


@bp_post.route('/new/<string:user_id>', methods=['GET', 'POST'])
@login_required
def new_post(user_id):
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

        if type_publication == 'public':
            Post(user_data["email"], subject, content, type_publication=type_publication).insert(_type=type_publication)

        elif type_publication == 'uplines' or type_publication == 'upline':
            user = User.find_by_id(user_id)
            uplines = user.find_uplines()
            if uplines:
                post = Post(user_data["email"], subject, content,type_publication=type_publication)
                post.insert(type_publication)
                for up in uplines:
                    Post.connect(up["email"], post._id, type_publication)
            else:
                flash("You have not any uplines.")
                return redirect(url_for('posts.new_post', user_id=user_id))

        elif type_publication == 'subsets':
            subsets = User.find_sub(user_id)
            if subsets:
                post = Post(user_data["email"], subject, content, type_publication=type_publication)
                post.insert(type_publication)
                for sub in subsets:
                    Post.connect(sub["email"], post._id, type_publication)
            else:
                flash("You have not any subsets.")
                return redirect(url_for('posts.new_post', user_id=user_id))

        elif type_publication == 'directs':
            directs = User.find_directs(session["email"])
            if directs:
                post = Post(user_data["email"], subject, content, type_publication=type_publication)
                post.insert(type_publication)
                for direct in directs:
                    print(direct.email)
                    Post.connect(direct.email, post._id, type_publication)
            else:
                flash("You have not any directs.")
                return redirect(url_for('posts.new_post', user_id=user_id))

        return redirect(url_for('posts.view_sent_posts', user_id=user_data["_id"]))

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
@login_required
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
@login_required
def view_public_posts():
    """
    View all public post sent by everyone.
    :return: A page of all public posts.
    """
    posts = Post.find_all_public()
    message = "There is no public posts."
    return render_template('post/public_posts.html',
                           posts=posts,
                           title='Public posts', msg=message)


@bp_post.route('/from_subsets/<string:user_id>')
@login_required
def posts_from_subsets(user_id):
    user = User.find_by_id(user_id)
    posts = Post.find_message_by_type(user.email, 'uplines')
    message = "There is no posts from subsets."
    return render_template("post/public_posts.html",
                           posts=posts,
                           title='Posts from subsets', msg=message)


@bp_post.route('/from_uplines/<string:user_id>')
@login_required
def posts_from_uplines(user_id):
    user = User.find_by_id(user_id)
    posts = Post.find_message_by_type(user.email, 'subsets')
    message = "There is no posts from uplines."
    return render_template("post/public_posts.html",
                           posts=posts,
                           title='Posts from uplines', msg=message)


@bp_post.route('/for_directs/<string:user_id>')
@login_required
def posts_for_directs(user_id):
    user = User.find_by_id(user_id)
    posts = Post.find_message_by_type(user.email, 'directs')
    message = "There is no posts for directs."
    return render_template("post/public_posts.html",
                           posts=posts,
                           title='Posts for directs', msg=message)
