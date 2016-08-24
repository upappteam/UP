import os
import khayyam
from uuid import uuid4
from py2neo import Graph, Node, Relationship
from py2neo.ext.calendar import GregorianCalendar
from werkzeug.security import generate_password_hash, check_password_hash


graph = Graph()


class User:

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def find(self):
        user = graph.find_one(label='User',
                              property_key='phone_number',
                              property_value=self.phone_number)
        return user

    def register(self, password, upline_phone_number, company=None, gender=None,
                 email=None, name=None, family_name=None, birthday=None, bio=None):

        if not self.find():
            register_date = khayyam.JalaliDate.today().strftime("%A %d %B %Y")
            _id = uuid4().hex

            user = Node('User', phone_number=self.phone_number,
                        password=generate_password_hash(password, salt_length=32),
                        upline_phone_number=upline_phone_number,  family_name=family_name,
                        company=company, email=email, birthday=birthday, bio=bio,
                        register_date=register_date, _id=_id, name=name, gender=gender)

            graph.create(user)
            return True
        return False

    def verify_password(self, password):
        user = self.find()

        if user is not None:
            return check_password_hash(user["password"], password)

        return False

    @staticmethod
    def find_upline(upline_phone_number):
        upline = graph.find_one('User', 'phone_number', upline_phone_number)

        if upline is not None:
            return upline

        else:
            return False

    def connect_to_upline(self):
        user = self.find()
        upline = self.find_upline(user["upline_phone_number"])

        if upline and user["phone_number"] != upline["phone_number"]:
            upline_relationship = Relationship(upline, "DIRECT", user)
            graph.create(upline_relationship)
            return True

        else:
            return False

    @staticmethod
    def find_by_id(_id):
        user = graph.find_one(label='User',
                              property_key='_id',
                              property_value=_id)
        if user:
            return user

    def change_password(self, password):
        user = self.find()
        user["password"] = generate_password_hash(password)
        user.push()
        return True

    def update_info(self, company=None, gender=None, email=None,
                    name=None, family_name=None, birthday=None, bio=None):

        user = self.find()
        user["name"] = name
        user["family_name"] = family_name
        user["company"] = company
        user["gender"] = gender
        user["email"] = email
        user["birthday"] = birthday
        user["bio"] = bio
        user.push()
        return True

    @staticmethod
    def find_by_phone_number(phone_number):
        user = graph.find_one(label='User',
                              property_key='phone_number',
                              property_value=phone_number)

        if user:
            return user
