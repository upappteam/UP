from flask import Blueprint, render_template, request, session

from src.users.models import User
from src.users.forms import RegisterForm
import src.users.errors as UserError


bp_user = Blueprint('users', __name__)


@bp_user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        phone_number = form.phone_number.data
        password = form.password.data
        upline_phone_number = form.upline_phone_number.data

        try:
            if User.register_user(phone_number=phone_number,password=password,
                                  upline_phone_number=upline_phone_number):

                return render_template('index.html')
        except UserError.UserError as e:
            return e.message
    else:
        return render_template('user/register.html', form=form)


@bp_user.route('/uplines/<phone>')
def test(phone):
    s, b = User.find_uplines(phone)
    return 's: {0}\n b: {1}'.format(s, b)
