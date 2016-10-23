from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, SubmitField, fields


class RegisterForm(Form):
    phone_number = StringField(label='Phone Number',
                               validators=[validators.DataRequired('Please enter your phone number.')])
    upline_phone_number = StringField(label='Upline Phone Number',
                                      validators=[validators.DataRequired('Please enter your upline phone number.')])
    password = PasswordField(label='Password',
                             validators=[validators.DataRequired('Please enter your password.')])
    password_c = PasswordField(label='Confirm Password',
                               validators=[validators.DataRequired('Please enter your password again.')])
    work_alone = fields.BooleanField(label='Work alone',
                                     validators=[validators.optional()])

    # submit = SubmitField(label='Register',
    #                      validators=[validators.DataRequired()])


class LoginForm(Form):
    phone_number = StringField(label='Phone Number',
                               validators=[validators.DataRequired('Please enter your phone number.')])
    password = PasswordField(label='Password',
                             validators=[validators.DataRequired('Please enter your password.')])
    remember_me = fields.BooleanField(label='Remember me',
                                      validators=[validators.optional()])

    # submit = SubmitField(label='Log in',
    #                      validators=[validators.DataRequired()])
