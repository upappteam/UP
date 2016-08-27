import uuid
import khayyam
from py2neo import Graph, Relationship, Node

from src.users.models import User


uri = "http://localhost:7474/db/data/"
graph = Graph(uri)


class Post(object):

    def __init__(self, user_email, subject, text, publish_date=None, _id=None):
        self.user_email = user_email
        self.subject = subject
        self.text = text
        self.publish_date = khayyam.JalaliDatetime.today().strftime("%Y-%m-%d %H:%M:%S") if publish_date is None else publish_date
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
        posts = graph.find('Post', property_key="user", property_value=user_email)

        return [cls(**post_data) for post_data in posts]

    def insert(self):
        user_node = User.find_by_email(self.user_email)
        new_post = Node("Post", user_email=self.user_email,
                        subject=self.subject,
                        text=self.text,
                        publish_date=self.publish_date,
                        _id=self._id)
        graph.create(new_post)
        rel = Relationship(user_node, "PUBLISHED", new_post)
        graph.create(rel)
