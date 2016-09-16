import uuid
import khayyam3
# import py2neo
from py2neo import Graph, Relationship, Node

from src.users.models import User


graph = Graph()
# TODO Fix query for all function


class Post(object):

    def __init__(self, user_email, subject, content, timestamp='None', to='None', type_publication='None', publish_date=None, _id=None):
        self.user_email = user_email
        self.subject = subject
        self.content = content
        self.to = to
        self.type_publication = type_publication
        self.timestamo = timestamp
        self.publish_date = khayyam3.JalaliDatetime.today().strftime("%Y-%m-%d %H:%M:%S") if publish_date is None else publish_date
        self._id = uuid.uuid4().hex if _id is None else _id

    @staticmethod
    def find_one(_id):
        post_data = graph.find_one('Post', property_key="_id", property_value=_id)
        if post_data:
            return post_data

    @classmethod
    def classify(cls, post_data):
        post_data = Post.find_one(post_data["_id"])
        return cls(**post_data)

    @classmethod
    def find_all_by_email(cls, user_email):
        # posts = graph.find('Post', property_key="user_email", property_value=user_email)
        #
        # return [cls(**post_data) for post_data in posts]
        query = """
            MATCH (user:User)-[:PUBLISHED]->(post:Post)
            WHERE user.email = {user_email}
            RETURN post
            ORDER BY post.timestamp DESC
        """
        posts = graph.data(query, user_email=user_email)

        if posts:
            post_list = []
            for post in posts:
                post_list += [cls(**post[i]) for i in post]

            return post_list

    def insert(self, _type):
        user_node = User.find_by_email(self.user_email)
        new_post = Node("Post", user_email=self.user_email,
                        subject=self.subject,
                        content=self.content,
                        to="None",
                        timestamp=int(khayyam3.JalaliDatetime.today().strftime("%Y%m%d%H%M%S")),
                        type_publication=self.type_publication,
                        publish_date=self.publish_date,
                        _id=self._id)
        graph.create(new_post)
        rel = Relationship(user_node, "PUBLISHED", new_post, type=_type)
        graph.create(rel)

    @staticmethod
    def delete(_id, user):
        post = Post.find_one(_id)
        rel = graph.match_one(user, "PUBLISHED", post)

        graph.separate(rel)
        graph.delete(post)

    @staticmethod
    def edit(_id, subject, content):
        post = Post.find_one(_id)
        post["subject"] = subject
        post["content"] = content
        post["publish_date"] = khayyam3.JalaliDatetime.today().strftime("%Y-%m-%d %H:%M:%S")
        post["timestamp"] = int(khayyam3.JalaliDatetime.today().strftime("%Y%m%d%H%M%S"))
        post.push()

    # @classmethod
    # def find_all_public(cls):
    #     posts = graph.find("Post", property_key="type_publication", property_value="public")
    #     return [cls(**post) for post in posts]

    @classmethod
    def find_all_type(cls, user_email, _type):
        query = """
            MATCH (user:User)-[:PUBLISHED{type: {_type}}]->(post:Post)
            WHERE user.email = {user_email}
            RETURN post
            ORDER BY post.timestamp DESC
        """
        posts = graph.data(query, user_email=user_email, _type=_type)

        if posts:
            post_list = []
            for post in posts:
                post_list += [cls(**post[i]) for i in post]

            return post_list

    def insert_pv(self, to, user_email):
        user_node = User.find_by_email(self.user_email)
        new_post = Node("Post", user_email=self.user_email,
                        subject=self.subject,
                        content=self.content,
                        to=to,
                        type_publication=self.type_publication,
                        publish_date=self.publish_date,
                        _id=self._id)

        graph.create(new_post)
        rel1 = Relationship(user_node, "PUBLISHED", new_post)
        graph.create(rel1)

        user = User.find_by_email(user_email)
        rel2 = Relationship(new_post, "MESSAGE", user)
        graph.create(rel2)

    @classmethod
    def find_message(cls, user_email):
        # posts = graph.find("Post", property_key="to", property_value=user_email)
        # return [cls(**post) for post in posts]
        query = """
            MATCH (p:Post)-[:MESSAGE]->(:User)
            WHERE p.to = {user_email}
            RETURN p
            ORDER BY p.timestamp DESC
        """
        posts = graph.data(query, user_email=user_email)
        if posts:
            post_list = []
            for post in posts:
                post_list += [cls(**post[i]) for i in post]
            return post_list

    @staticmethod
    def delete_message_inbox(_id, user):
        post = Post.find_one(_id)
        rel = graph.match_one(post, "MESSAGE", user)
        print(rel)

        graph.separate(rel)

    @staticmethod
    def delete_message_outbox(_id, user):
        post = Post.find_one(_id)
        rel = graph.match_one(user, "PUBLISHED", post)
        print(rel)

        graph.separate(rel)

    @classmethod
    def find_all_public(cls):
        query = """
            MATCH (user:User)-[:PUBLISHED{type: {_type}}]->(post:Post)
            RETURN post
            ORDER BY post.timestamp DESC
        """
        posts = graph.data(query, _type='public')

        if posts:
            post_list = []
            for post in posts:
                post_list += [cls(**post[i]) for i in post]

            return post_list
