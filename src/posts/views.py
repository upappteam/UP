from flask import Blueprint


bp_post = Blueprint('posts', __name__)


@bp_post.route('/<string:user_id>')
def view_pasts(user_id):
    pass
