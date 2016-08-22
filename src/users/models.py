import os
from werkzeug.security import generate_password_hash
from py2neo import Graph, Node, Relationship


graph = Graph()


class User:

    def __init__(self, phone_number):
        self.phone_number = phone_number

    def find(self):
        user = graph.find_one(label='User',
                              property_key='phone_number',
                              property_value=self.phone_number)
        return user

    def register(self, password, upline_phone_number):
        if not self.find():
            user = Node('User', phone_number=self.phone_number,
                        password=generate_password_hash(password, salt_length=32),
                        upline_phone_number=upline_phone_number)

            graph.create(user)
            return True
        return False
