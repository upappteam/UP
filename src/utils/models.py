from passlib.hash import pbkdf2_sha512


class Utils(object):

    @staticmethod
    def set_password(password):
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_password(pw_hashed, password):
        return pbkdf2_sha512.verify(password, pw_hashed)
