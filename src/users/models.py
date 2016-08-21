import uuid
import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from src.common.database import Database
import src.users.constants as UserConstants
import src.users.errors as UserError


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
        Database.insert(collection=UserConstants.COLLECTION, data=self.json())

    def set_password(self, password):
        self.password = generate_password_hash(password, salt_length=32)

    @staticmethod
    def check_password(pw_hashed, password):
        return check_password_hash(pw_hashed, password)

    @classmethod
    def get_by_phone(cls, phone_number):
        user_data = Database.find_one(UserConstants.COLLECTION, {"phone_number": phone_number})
        return cls(**user_data)

    @classmethod
    def get_by_id(cls, _id):
        return cls(**Database.find_one(UserConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_by_email(cls, email):
        return cls(**Database.find(UserConstants.COLLECTION, {"email": email}))

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

    @staticmethod
    def remove_by_id(_id):
        Database.remove(UserConstants.COLLECTION, {"_id": _id})

    @staticmethod
    def register_user(phone_number, password, upline_phone_number):
        user_data = Database.find_one(UserConstants.COLLECTION, {"phone_number": phone_number})
        upline = Database.find_one(UserConstants.COLLECTION,
                                   {"upline_phone_number": upline_phone_number})

        if user_data is not None:
            raise UserError.UserAlreadyRegisteredError("This user already exist.")

        if upline is None:
            raise UserError.UplineNotExistsError("The upline phone number is wrong.")

        User(phone_number=phone_number,
             password=password,
             upline_phone_number=upline_phone_number).save_to_db()

        return True
