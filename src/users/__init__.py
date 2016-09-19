from flask import Blueprint


bp_user = Blueprint('users', __name__)

from . import views
