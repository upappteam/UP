from flask import Blueprint


bp_post = Blueprint('posts', __name__)

from . import views
