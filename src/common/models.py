from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps


def just_current_user(func):

    @wraps(func)
    def decorated_view(user_id,*args, **kwargs):
        if user_id == current_user._id:
            return func(user_id,*args, **kwargs)
        else:
            flash("you can't access to this page.")
            return redirect(url_for('users.home', user_id=current_user._id))

    return decorated_view
