from flask import Flask, render_template

from src.users.views import bp_user


app = Flask(__name__)

app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

app.register_blueprint(bp_user, url_prefix='/users')


