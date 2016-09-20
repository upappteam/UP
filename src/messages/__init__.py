from flask import Blueprint


bp_message = Blueprint('messages', __name__)

from . import views
