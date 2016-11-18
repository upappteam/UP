from flask import abort
from functools import wraps
from flask_login import current_user


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLE = 0x04
    MODERATOR = 0x08
    ADMINISTER = 0x80


class Role:
    pass


def permission_require(permission):

    def decorator(func):

        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator


def admin_require(func):
    return permission_require(Permission.ADMINISTER)
