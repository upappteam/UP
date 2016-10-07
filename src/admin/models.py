import uuid
from py2neo import Graph, Node
from flask_login import UserMixin

from src.posts.models import Post
from src.users.models import User


graph = Graph()


class Admin(UserMixin, object):

    def __init__(self, name, family, email, password, _id=None):
        self.name = name
        self.family = family
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def init_neo4j(self):
        admin = graph.find_one('Admin', property_key='email', property_value=self.email)
        if admin:
            return
        else:
            admin = Node('Admin',
                         name=self.name,
                         family=self.family,
                         email=self.email,
                         password=self.password,
                         _id=self._id)

            graph.create(admin)

    @classmethod
    def classify(cls, admin_data):
        return cls(name=admin_data["name"],
                   family=admin_data["family"],
                   email=admin_data["email"],
                   password=admin_data["password"],
                   _id=admin_data["_id"])

    @staticmethod
    def find_admin_id(_id):
        admin = graph.find_one('Admin', property_key='_id', property_value=_id)
        if admin:
            return admin

    @staticmethod
    def find_admin_email(email):
        admin = graph.find_one('Admin', property_key='email', property_value=email)
        if admin:
            return admin

    def get_id(self):
        return self._id

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @staticmethod
    def find_all_public_posts():
        query = """
                    MATCH (:User)-[:PUBLISHED{type: {_type}}]->(post:Post)
                    RETURN post
                    ORDER BY post.timestamp DESC
                """
        posts = graph.data(query, _type='public')
        if posts:
            posts_list = []
            for post in posts:
                posts_list += [Post(**post[i]) for i in post]
            return posts_list

    @staticmethod
    def find_all_private_posts():
        query = """
                    MATCH (:User)-[:PUBLISHED{type: {_type}}]->(post:Post)
                    RETURN post
                    ORDER BY post.timestamp DESC
                """
        posts = graph.data(query, _type='private')
        if posts:
            posts_list = []
            for post in posts:
                posts_list += [Post(**post[i]) for i in post]
            return posts_list

    @staticmethod
    def find_all_subsets_posts():
        query = """
                    MATCH (:User)-[:PUBLISHED{type: {_type}}]->(post:Post)
                    RETURN post
                    ORDER BY post.timestamp DESC
                """
        posts = graph.data(query, _type='subsets')
        if posts:
            posts_list = []
            for post in posts:
                posts_list += [Post(**post[i]) for i in post]
            return posts_list

    @staticmethod
    def find_all_uplines_posts():
        query = """
                    MATCH (:User)-[:PUBLISHED{type: {_type}}]->(post:Post)
                    RETURN post
                    ORDER BY post.timestamp DESC
                """
        posts = graph.data(query, _type='uplines')
        if posts:
            posts_list = []
            for post in posts:
                posts_list += [Post(**post[i]) for i in post]
            return posts_list

    @staticmethod
    def find_all_directs_posts():
        query = """
                    MATCH (:User)-[:PUBLISHED{type: {_type}}]->(post:Post)
                    RETURN post
                    ORDER BY post.timestamp DESC
                """
        posts = graph.data(query, _type='directs')
        if posts:
            posts_list = []
            for post in posts:
                posts_list += [Post(**post[i]) for i in post]
            return posts_list

    @staticmethod
    def find_all_upline_posts():
        query = """
                    MATCH (:User)-[:PUBLISHED{type: {_type}}]->(post:Post)
                    RETURN post
                    ORDER BY post.timestamp DESC
                """
        posts = graph.data(query, _type='upline')
        if posts:
            posts_list = []
            for post in posts:
                posts_list += [Post(**post[i]) for i in post]
            return posts_list

    @staticmethod
    def find_all_users():
        query = """
                    MATCH (user:User)
                    RETURN user
                    ORDER BY user.name ASC
                """
        users = graph.data(query)
        if users:
            users_list = []
            for user in users:
                users_list += [User(**user[i]) for i in user]
            return users_list

    @staticmethod
    def find_user_by_email(email):
        user = graph.find_one('User', property_key='email', property_value=email)
        if user:
            return user

    @staticmethod
    def find_user_subsets_by_email(email):
        query = """
                    MATCH (user1:User)-[:DIRECT*1..]->(user2:User)
                    WHERE user1.email = {email}
                    RETURN user2
                    ORDER BY user.name ASC
                """
        users = graph.data(query, email=email)
        if users:
            users_list = []
            for user in users:
                users_list += [Post(**user[i]) for i in user]
            return users_list

    @staticmethod
    def find_user_uplines_by_email(email):
        query = """
                    MATCH (user1:User)-[:UPLINE*1..]->(user2:User)
                    WHERE user1.email = {email}
                    RETURN user2
                    ORDER BY user.name ASC
                """
        users = graph.data(query, email=email)
        if users:
            users_list = []
            for user in users:
                users_list += [Post(**user[i]) for i in user]
            return users_list
