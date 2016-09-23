from flask import Blueprint


bp_admin = Blueprint('admins', __name__)

from . import views
