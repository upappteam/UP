from flask import Flask

from src.users.views import bp_user
from src.common.database import Database


app = Flask(__name__)

app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

app.register_blueprint(bp_user, url_prefix='/users')


@app.before_first_request
def initialize():
    Database.initialize()
