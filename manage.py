#!/usr/bin/env python3
import os
from py2neo import Graph
from flask_script import Manager, Shell

from src import create_app
from src.users.models import User
from src.posts.models import Post
from src.admin.models import Admin


app = create_app(os.getenv('UP_CONFIG') or 'default')
manager = Manager(app)


def shell_context():
    return dict(app=app, User=User, Post=Post, Admin=Admin)

manager.add_command('shell', Shell(make_context=shell_context))

if __name__ == '__main__':
    manager.run()
