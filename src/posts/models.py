import uuid
import khayyam3
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
        self.timestamp = timestamp
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
            MATCH (user:User)-[sent:PUBLISHED]->(post:Post)
            WHERE user.email = {user_email} AND sent.type <> {_type}
            RETURN post
            ORDER BY post.timestamp DESC
        """
        posts = graph.data(query, user_email=user_email, _type='private')

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

    def insert_by_type(self, to, user_email, _type):
        user_node = User.find_by_email(self.user_email)
        new_post = Node("Post", user_email=self.user_email,
                        subject=self.subject,
                        content=self.content,
                        to=to,
                        type_publication=self.type_publication,
                        publish_date=self.publish_date,
                        _id=self._id)

        graph.create(new_post)
        rel1 = Relationship(user_node, "PUBLISHED", new_post, type=_type)
        graph.create(rel1)

        user = User.find_by_email(user_email)
        rel2 = Relationship(new_post, "MESSAGE", user, type=_type)
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
        # print(rel)

        graph.separate(rel)

    @staticmethod
    def delete_message_outbox(_id, user):
        post = Post.find_one(_id)
        rel = graph.match_one(user, "PUBLISHED", post)
        # print(rel)

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

    @staticmethod
    def connect(user_email, post_id, _type):
        user = User.find_by_email(user_email)
        post = Post.find_one(post_id)
        rel = Relationship(post, "MESSAGE", user, type=_type)
        graph.create(rel)

    @staticmethod
    def disconnect(user_email, post_id, _type):
        user = User.find_by_email(user_email)
        post = Post.find_one(post_id)
        rel = Relationship(post, "MESSAGE", user, type=_type)
        graph.separate(rel)

    @classmethod
    def find_message_by_type(cls, user_email, _type):
        query = """
            MATCH (post:Post)-[:MESSAGE{type: {_type}}]->(user:User)
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

    @classmethod
    def admin_find_posts_by_author(cls, author):
        query = """
            MATCH (post:Post)
            WHERE post.user_email = {author}
            RETURN post
            ORDER BY post.timestamp DESC
        """
        posts = graph.data(query, author=author)
        if posts:
            posts_list = []
            for post in posts:
                posts_list += [cls(**post[i]) for i in post]
            return posts_list

    @classmethod
    def admin_find_posts_by_date(cls, *args):
        if len(args) == 1:
            main_query = """
                            MATCH (post:Post)
                            RETURN post
                         """
            posts = graph.data(main_query)
            if posts:
                post_list = []
                date = khayyam3.JalaliDatetime.strptime(args[0], "%Y")
                for post in posts:
                    temp = [cls(**post[i]) for i in post]
                    if khayyam3.JalaliDatetime.strptime(str(temp[0].publish_date[:4]), "%Y") >= date:
                        post_list += [cls(**post[i]) for i in post]
                return post_list

        elif len(args) == 2:
            main_query = """
                            MATCH (post:Post)
                            RETURN post
                         """
            posts = graph.data(main_query)
            if posts:
                post_list = []
                date = khayyam3.JalaliDatetime.strptime(args[0] + "-" + args[1], "%Y-%m")
                for post in posts:
                    temp = [cls(**post[i]) for i in post]
                    if khayyam3.JalaliDatetime.strptime("-".join(temp[0].publish_date.split(" ")[0].split("-")[:2]), "%Y-%m") >= date:
                        post_list += [cls(**post[i]) for i in post]
                return post_list

        elif len(args) == 3:
            main_query = """
                            MATCH (post:Post)
                            RETURN post
                         """
            posts = graph.data(main_query)
            if posts:
                post_list = []
                date = khayyam3.JalaliDatetime.strptime(args[0] + "-" + args[1] + "-" + args[2], "%Y-%m-%d")
                for post in posts:
                    temp = [cls(**post[i]) for i in post]
                    if khayyam3.JalaliDatetime.strptime("-".join(temp[0].publish_date.split(" ")[0].split("-")[:]), "%Y-%m-%d") >= date:
                        post_list += [cls(**post[i]) for i in post]
                return post_list

        elif len(args) == 4:
            main_query = """
                            MATCH (post:Post)
                            RETURN post
                         """
            posts = graph.data(main_query)
            if posts:
                post_list = []
                date = khayyam3.JalaliDatetime.strptime(args[0] + "-" + args[1] + "-" + args[2] + "-" + args[3],
                                                        "%Y-%m-%d-%H")
                for post in posts:
                    temp = [cls(**post[i]) for i in post]
                    if khayyam3.JalaliDatetime.strptime("-".join(temp[0].publish_date.split(" ")[0].split("-")[:]) + " " + "".join(temp[0].publish_date.split(" ")[1].split(":")[0]), "%Y-%m-%d %H") >= date:
                        post_list += [cls(**post[i]) for i in post]
                return post_list

    @classmethod
    def admin_find_posts_by_title(cls, *args):
        if len(args) == 1:
            query = """
                        MATCH (post:Post)
                        RETURN post
                        ORDER BY post.timestamp DESC
                    """
            posts = graph.data(query)
            if posts:
                post_list = []
                for post in posts:
                    temp = [cls(**post[i]) for i in post]
                    if args[0] in temp[0].subject:
                        post_list += [cls(**post[i]) for i in post]
                return post_list

        elif len(args) > 1:
            all_list = []
            query = """
                            MATCH (post:Post)
                            RETURN post
                            ORDER BY post.timestamp DESC
                        """
            posts = graph.data(query)
            if posts:
                for title in args:
                    for post in posts:
                        temp = [cls(**post[i]) for i in post]
                        if title in temp[0].subject:
                            all_list += [cls(**post[i]) for i in post]
            return all_list

    @classmethod
    def admin_find_posts_by_content(cls, *args):
        if len(args) == 1:
            query = """
                        MATCH (post:Post)
                        RETURN post
                        ORDER BY post.timestamp DESC
                    """
            posts = graph.data(query, content=args[0])
            if posts:
                post_list = []
                for post in posts:
                    temp = [cls(**post[i]) for i in post]
                    if args[0] in temp[0].content:
                        post_list += [cls(**post[i]) for i in post]
                return post_list

        elif len(args) > 1:
            all_list = []
            query = """
                            MATCH (post:Post)
                            RETURN post
                            ORDER BY post.timestamp DESC
                        """
            posts = graph.data(query)
            for content in args:
                if posts:
                    for post in posts:
                        temp = [cls(**post[i]) for i in post]
                        if content in temp[0].subject:
                            all_list += [cls(**post[i]) for i in post]
            return all_list

    @classmethod
    def admin_find_all_posts_by_type(cls, _type):
        query = """
                    MATCH (post:Post)
                    WHERE post.type_publication = {_type}
                    RETURN post
                    ORDER BY post.timestamp DESC
                """
        posts = graph.data(query, _type=_type)
        if posts:
            post_list = []
            for post in posts:
                post_list += [cls(**post[i]) for i in post]
            return post_list

    @classmethod
    def admin_find_all_posts(cls):
        query = """
                    MATCH (post:Post)
                    RETURN post
                    ORDER BY post.timestamp DESC
                """
        posts = graph.data(query)
        if posts:
            post_list = []
            for post in posts:
                post_list += [cls(**post[i]) for i in post]
            return post_list

    @classmethod
    def admin_sent_posts(cls, admin_email):
        query = """
                    MATCH (post:Post)
                    WHERE post.user_email = {admin}
                    RETURN post
                    ORDER BY post.timestamp
                """
        posts = graph.data(query, admin=admin_email)
        if posts:
            post_list = []
            for post in posts:
                post_list += [cls(**post[i]) for i in post]
            return post_list

    def admin_insert_post_by_type(self, admin_node, to, _type):
        new_post = Node("Post", user_email=admin_node["email"],
                        subject=self.subject,
                        content=self.content,
                        to=to,
                        type_publication=self.type_publication,
                        publish_date=self.publish_date,
                        _id=self._id)

        graph.create(new_post)
        rel1 = Relationship(admin_node, "PUBLISHED", new_post, type=_type)
        graph.create(rel1)

        user = User.find_by_email(to)
        rel2 = Relationship(new_post, "MESSAGE", user, type=_type)
        graph.create(rel2)

    def admin_insert_post(self, admin_node, _type):
        new_post = Node("Post", user_email=admin_node["email"],
                        subject=self.subject,
                        content=self.content,
                        to="all",
                        timestamp=int(khayyam3.JalaliDatetime.today().strftime("%Y%m%d%H%M%S")),
                        type_publication=self.type_publication,
                        publish_date=self.publish_date,
                        _id=self._id)
        graph.create(new_post)
        rel = Relationship(admin_node, "PUBLISHED", new_post, type=_type)
        graph.create(rel)
