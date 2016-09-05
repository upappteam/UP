from flask import Blueprint, render_template, request, session, redirect, url_for

from src.users.models import User
from src.posts.models import Post
from src.posts.forms import PostForm


bp_post = Blueprint('posts', __name__)


@bp_post.route('/<string:user_id>')
def view_posts(user_id):
    user_data = User.find_by_id(user_id)
    # user = User.classify2(user_data)
    posts = Post.find_all_by_email(user_data.email)
    return render_template('post/view_posts.html', posts=posts, user_id=user_data._id)


@bp_post.route('/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if request.method == 'POST':
        subject = form.subject.data
        content = form.content.data
        user_data = User.find_by_email(session["email"])
        # user = User.classify(user_data)
        Post(user_data["email"], subject, content).insert()
        return redirect(url_for('posts.view_posts', user_id=user_data["_id"]))

    return render_template("post/new_post.html", form=form)
