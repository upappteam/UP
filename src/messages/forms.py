from flask_wtf import Form
from wtforms import StringField, TextAreaField, validators, SubmitField


class NewMessage(Form):
    subject = StringField(label='Subject',
                          validators=[validators.DataRequired("Enter message subject.")])
    to = StringField(label='To',
                     validators=[validators.DataRequired("Enter phone number or email address.")])
    content = TextAreaField(label='Message',
                            validators=[validators.DataRequired("Enter message content.")])

    submit = SubmitField(label='Send')
