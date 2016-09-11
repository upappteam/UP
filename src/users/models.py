import uuid
import khayyam3
from py2neo import Graph, Node, Relationship

import src.users.constants as UserConst
from src.users.utils import Utils


graph = Graph()


class User(object):

    def __init__(self, phone_number, upline_phone_number, password, company='None',
                 gender='None', email='None', name='None', family='None', birthday='None',
                 account_time='None', account_type='None', register_date=None, _id=None):

        self.phone_number = phone_number
        self.upline_phone_number = upline_phone_number
        self.password = password
        self.company = company
        self.gender = gender
        self.email = email
        self.name = name
        self.family = family
        self.birthday = birthday
        self.account_time = account_time
        self.account_type = account_type
        self.register_date = khayyam3.JalaliDatetime.today().strftime("%Y-%m-%d %H:%M:%S") if register_date is None else register_date
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def find_one(phone_number):
        user_data = graph.find_one(UserConst.USER, 'phone_number', phone_number)
        return user_data

    @staticmethod
    def find_by_email(user_email):
        user_data = graph.find_one(UserConst.USER, 'email', user_email)
        return user_data

    @classmethod
    def classify1(cls, user_data):
        return cls(phone_number=user_data["phone_number"],
                   upline_phone_number=user_data["upline_phone_number"],
                   password=user_data["password"],
                   company=user_data["company"],
                   gender=user_data["gender"],
                   email=user_data["email"],
                   name=user_data["name"],
                   family=user_data["family"],
                   birthday=user_data["birthday"],
                   account_time=user_data["account_time"],
                   account_type=user_data["account_type"],
                   register_date=user_data["register_date"],
                   _id=user_data["_id"])

    def classify_by_self(self):
        user_data = graph.find_one(UserConst.USER, "email", self.email)
        return User(phone_number=user_data.phone_number,
                    upline_phone_number=user_data["upline_phone_number"],
                    password=user_data["password"],
                    company=user_data["company"],
                    gender=user_data["gender"],
                    email=user_data["email"],
                    name=user_data["name"],
                    family=user_data["family"],
                    account_time=user_data["account_time"],
                    account_type=user_data["account_type"],
                    birthday=user_data["birthday"],
                    register_date=user_data["register_date"],
                    _id=user_data["_id"])

    def register(self):
        user_date = User.find_one(self.phone_number)
        if not user_date:
            new_user = Node(UserConst.USER,
                            phone_number=self.phone_number,
                            upline_phone_number=self.upline_phone_number,
                            password=self.password,
                            company=self.company,
                            gender=self.gender,
                            email=self.email,
                            name=self.name,
                            family=self.family,
                            birthday=self.birthday,
                            register_date=self.register_date,
                            account_time=self.account_time,
                            account_type=self.account_type,
                            _id=self._id)

            graph.create(new_user)

            return True
        return False

    def connect_to_upline(self):
        user = User.find_one(self.phone_number)
        upline = User.find_one(self.upline_phone_number)

        if user["phone_number"] != upline["phone_number"]:
            rel_d = Relationship(upline, "DIRECT", user)
            graph.create(rel_d)
            rel_u = Relationship(user, "UPLINE", upline)
            graph.create(rel_u)

            return True

        return False

    @classmethod
    def find_by_id(cls, _id):
        user_data = graph.find_one(UserConst.USER, property_key='_id', property_value=_id)
        if user_data:
            return cls(phone_number=user_data["phone_number"],
                       upline_phone_number=user_data["upline_phone_number"],
                       password=user_data["password"],
                       company=user_data["company"],
                       gender=user_data["gender"],
                       email=user_data["email"],
                       name=user_data["name"],
                       family=user_data["family"],
                       birthday=user_data["birthday"],
                       account_time=user_data["account_time"],
                       account_type=user_data["account_type"],
                       register_date=user_data["register_date"],
                       _id=user_data["_id"])

    def update_info(self, email, password):
        user_data = User.find_one(self.phone_number)

        user_data["email"] = email
        user_data["password"] = Utils.set_password(password)

        user_data.push()
        return True

    @staticmethod
    def valid_phone_number(phone_number):
        user = User.find_one(phone_number)
        if user:
            return True
        return False

    def profile(self, name, family, gender, company, email, birthday):
        user = User.find_one(self.phone_number)
        user["name"] = name
        user["family"] = family
        user["gender"] = gender
        user["company"] = company
        user["email"] = email
        user["birthday"] = birthday

        user.push()

    def change_password(self, new_password):
        user = User.find_one(self.phone_number)
        user["password"] = Utils.set_password(new_password)

        user.push()

    @staticmethod
    def find_sub(_id):
        user = User.find_by_id(_id)

        sub_list = [sub_user for sub_user in graph.find(UserConst.USER,
                                                        property_key="upline_phone_number",
                                                        property_value=user.phone_number)]
        if sub_list:
            main = sub_list[:]

            while True:
                sub = sub_list[0]
                sub_list = sub_list[1:]
                sub_list += [sub_user for sub_user in graph.find(UserConst.USER,
                                                                 property_key="upline_phone_number",
                                                                 property_value=sub["phone_number"]) if sub_user is not None]

                main += sub_list
                if sub_list is None or len(sub_list) < 1:
                    main = set(main)
                    break
            if main:
                # for i in main:
                    # print(i["phone_number"])
                count = len(main)
                # print(count)
                return main, count

        else:
            # print("You have not subset yet!")
            return None, 0

    def find_uplines(self):
        upline = graph.find_one(UserConst.USER, 'phone_number', self.upline_phone_number)

        if upline:
            main = []
            main.append(upline)
            up = upline

            while True:
                upline = graph.find_one(UserConst.USER, "phone_number",
                                        up["upline_phone_number"])
                if upline:
                    main.append(upline)
                    up = upline
                else:
                    break

            return main

        return []