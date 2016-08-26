from werkzeug.security import generate_password_hash, check_password_hash


class Utils(object):

    @staticmethod
    def set_password(password):
        return generate_password_hash(password, salt_length=32)

    @staticmethod
    def check_password(pw_hashed, password):
        return check_password_hash(pw_hashed, password)
