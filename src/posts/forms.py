from flask_wtf import Form
from wtforms import StringField, TextAreaField, validators, SubmitField, DateField


class PostForm(Form):

    subject = StringField(label='Subject', validators=[validators.DataRequired("The post subject.")])
    # date = DateField(label='Publish Date', validators=[validators.DataRequired("The post date")])
    content = TextAreaField(label='Post', validators=[validators.DataRequired("The text post.")])

    submit = SubmitField(label='Publish')
