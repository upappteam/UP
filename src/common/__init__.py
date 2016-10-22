from flask import Blueprint


bp_common = Blueprint('common', __name__)

from . import views
