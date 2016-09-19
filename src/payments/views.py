from flask import Blueprint

from src.users.models import User


bp_accounts = Blueprint('payments', __name__)


@bp_accounts.route('/new/<string:user_id>')
def new_account(user_id):
    # user = User.find_by_id(user_id)
    pass
