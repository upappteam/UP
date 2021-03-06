import uuid

import khayyam3
from flask_login import UserMixin
from py2neo import Graph, Node, Relationship

import config
from src.users.constants import USER
from src.utils.models import Utils

graph = Graph(config.Develop.URI)


class User(UserMixin, object):

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
        user_data = graph.find_one(USER, 'phone_number', phone_number)
        return user_data

    @staticmethod
    def find_by_email(user_email):
        user_data = graph.find_one(USER, 'email', user_email)
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
        user_data = graph.find_one(USER, "email", self.email)
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
            new_user = Node(USER,
                            phone_number=self.phone_number,
                            upline_phone_number=self.upline_phone_number,
                            password=self.password,
                            company=self.company,
                            gender=self.gender,
                            email=self.email.lower(),
                            name=self.name.lower(),
                            family=self.family.lower(),
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
        user_data = graph.find_one(USER, property_key='_id', property_value=_id)
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

    @classmethod
    def find_sub(cls, _id):
        # sub_list = [sub_user for sub_user in graph.find(USER,
        #                                                 property_key="upline_phone_number",
        #                                                 property_value=user.phone_number)]
        # if sub_list:
        #     main = sub_list[:]
        #
        #     while True:
        #         sub = sub_list[0]
        #         sub_list = sub_list[1:]
        #         sub_list += [sub_user for sub_user in graph.find(USER,
        #                                                          property_key="upline_phone_number",
        #                                                          property_value=sub["phone_number"]) if sub_user is not None]
        #
        #         main += sub_list
        #         if sub_list is None or len(sub_list) < 1:
        #             main = set(main)
        #             break
        #     if main:
        #         return main
        #
        # else:
        #     return []
        user = User.find_by_id(_id)
        query = """
            MATCH (user1:User)-[:DIRECT*1..]->(user2:User)
            WHERE user1._id = {_id}
            RETURN user2
        """
        users = graph.data(query, _id=_id)
        if users:
            users_list = []
            for user in users:
                users_list += [cls(**user[i]) for i in user]
            return users_list

    @classmethod
    def find_uplines(cls, _id):
        # upline = graph.find_one(USER, 'phone_number', self.upline_phone_number)
        #
        # if upline:
        #     main = []
        #     main.append(upline)
        #     up = upline
        #
        #     while True:
        #         upline = graph.find_one(USER, "phone_number",
        #                                 up["upline_phone_number"])
        #         if upline:
        #             main.append(upline)
        #             up = upline
        #         else:
        #             break
        #
        #     return main
        #
        # return []
        query = """
            MATCH (user1:User)-[:UPLINE*1..]->(user2:User)
            WHERE user1._id = {_id}
            RETURN user2
        """
        users = graph.data(query, _id=_id)
        if users:
            users_list = []
            for user in users:
                users_list += [cls(**user[i]) for i in user]
            return users_list

    @classmethod
    def find_directs(cls, user_email):
        query = """
            MATCH (user1:User)-[:DIRECT]->(user2:User)
            WHERE user1.email = {user_email}
            RETURN user2
        """
        directs = graph.data(query, user_email=user_email)
        if directs:
            direct_list = []
            for direct in directs:
                direct_list += [cls(**direct[i]) for i in direct]
            return direct_list

    def get_id(self):
        return self._id

    @classmethod
    def search_by_name_family(cls, name, family):
        query = """
            MATCH (user:User)
            WHERE (user.name = {name} AND user.family = {family}) OR (user.name = {name})
            OR (user.family = {family})
            RETURN user
        """

        users = graph.data(query, name=name, family=family)
        if users:
            users_list = []
            for user in users:
                users_list += [cls(**user[i]) for i in user]
            return users_list

    # @classmethod
    # def search_by_email(cls, email):
    #     query = """
    #         MATCH (user:User)
    #         WHERE user.email = {email}
    #         RETURN user
    #     """
    #     user

    @classmethod
    def admin_find_all_users(cls):
        query = """
                    MATCH (user:User)
                    RETURN user
                """
        users = graph.data(query)
        if users:
            user_list = []
            for user in users:
                user_list += [cls(**user[i]) for i in user]
            return user_list

    @staticmethod
    def check_follow_relation(current_user_id, another_user_id):
        query = """
                    MATCH (current:User)-[follow:FOLLOW]->(another:User)
                    WHERE (current._id = {current_user_id}) AND (another._id = {another_user_id})
                    RETURN follow
                """
        rel = graph.data(query, current_user_id=current_user_id, another_user_id=another_user_id)
        if rel:
            return True
        else:
            return False

    @staticmethod
    def follow_user(current_user_id, another_user_id):
        current_user_node = graph.find_one('User', property_key='_id', property_value=current_user_id)
        another_user_node = graph.find_one('User', property_key='_id', property_value=another_user_id)
        rel = Relationship(current_user_node, "FOLLOW", another_user_node)
        if current_user_id != another_user_id:
            graph.create(rel)

    @staticmethod
    def un_follow_user(current_user_id, another_user_id):
        current_user_node = graph.find_one('User', property_key='_id', property_value=current_user_id)
        another_user_node = graph.find_one('User', property_key='_id', property_value=another_user_id)

        rel = graph.match_one(current_user_node, "FOLLOW", another_user_node)
        print(rel)
        graph.separate(rel)
