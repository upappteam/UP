import uuid
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from src.common.database import Database
# import src.users.constants as UserConstants


class User(object):

    # user_counter = 0

    def __init__(self, phone_number, password, upline_phone_number,
                 company=None, email=None, name=None, family_name=None,
                 birthday=None, register_date=datetime.datetime.utcnow(), _id=None):

        self.phone_number = phone_number
        self.set_password(password)
        self.upline_phone_number = upline_phone_number
        self.company = company
        self.email = email
        self.name = name
        self.family_name = family_name
        self.birthday = birthday
        self.register_date = register_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "phone_number": self.phone_number,
            "password": self.password,
            "upline_phone_number": self.upline_phone_number,
            "company": self.company,
            "email": self.email,
            "name": self.name,
            "family_name": self.family_name,
            "birthday": self.birthday,
            "register_date": self.register_date,
            "_id": self._id
        }

    def save_to_db(self):
        Database.insert(collection='users', data=self.json())

    def set_password(self, password):
        self.password = generate_password_hash(password, salt_length=32)

    @staticmethod
    def check_password(pw_hashed, password):
        return check_password_hash(pw_hashed, password)

    @classmethod
    def get_by_phone(cls, phone_number):
        user_data = Database.find_one('users', {"phone_number": phone_number})
        return cls(phone_number=user_data['phone_number'],
                   password=user_data['password'],
                   upline_phone_number=user_data['upline_phone_number'],
                   company = user_data['company'],
                   email = user_data['email'],
                   name = user_data['name'],
                   family_name = user_data['family_name'],
                   birthday = user_data['birthday'],
                   register_date = user_data['register_date'],
                   _id = user_data['_id']
                   )

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one('users', {"_id": _id}))

    @classmethod
    def get_by_email(cls, email):
        return cls(**Database.find('users', {"email": email}))

    @classmethod
    def find_uplines(cls, phone_number):
        counter = 0
        upline_list = []
        # while True:
        user = cls.get_by_phone(phone_number)
        upline = cls.get_by_phone(user.upline_phone_number)
        upline_list.append(upline.phone_number)
        # phone_number = upline.phone_number
        counter += 1
        # if upline.phone_number == '' or upline.phone_number == None:
        #     break
        return counter, upline_list
