from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, SubmitField


class RegisterForm(Form):
    phone_number = StringField(label='Phone Number' , validators=[validators.DataRequired('Please enter your phone number')])
    upline_phone_number = StringField(label='Upline Phone Number' , validators=[validators.optional()])
    password = PasswordField(label='password' , validators=[validators.required()])
    submit = SubmitField(label='Register' , validators=[validators.required()])
