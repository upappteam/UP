from flask import render_template
from src import create_app


app = create_app('develop')


@app.route('/')
def index():
    return render_template('index.html')
