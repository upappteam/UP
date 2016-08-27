from flask import Flask, render_template

from src.users.views import bp_user
from src.posts.views import bp_post


app = Flask(__name__)

app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

app.register_blueprint(bp_user, url_prefix='/users')
app.register_blueprint(bp_post, url_prefix='/posts')


@app.route('/')
def index():
    return render_template('index.html')
