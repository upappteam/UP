from flask import Blueprint, render_template, request, session

from src.users.forms import RegisterForm
from src.users.models import User


bp_user = Blueprint('users', __name__)


@bp_user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        new_user = User(phone_number=form.phone_number.data,
                        upline_phone_number=form.upline_phone_number.data,
                        password=form.password.data)

        # session['name'] = new_user.name
        new_user.save_to_db()
        return render_template('index.html')
    else:
        return render_template('user/register.html', form=form)


@bp_user.route('/uplines/<phone>')
def test(phone):
    s, b = User.find_uplines(phone)
    return 's: {0}\n b: {1}'.format(s, b)
