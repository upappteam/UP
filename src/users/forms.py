# import khayyam
from flask_wtf import Form
from wtforms import validators, StringField, PasswordField, SubmitField, SelectField, FormField, TextAreaField


# date_regex = '^(?:(?:31(\/|-|\.)(?:0?[123456]|(?:Farvardin|Ordibehesht|Khordad|Tir|Mordad|Shahrivar)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1-9]|1[0-2]|(?:Farvardin|Ordibehesht|Khordad|Tir|Mordad|Shahrivar|Mehr|Aban|Azar|Dey|Bahman|Esfand))\2))(?:(?:1[3-4]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[3-4]|[2-9]\d)?\d{2})$'


class RegisterForm(Form):
    phone_number = StringField(label='Phone Number',
                               validators=[validators.DataRequired('Please enter your phone number.')])
    upline_phone_number = StringField(label='Upline Phone Number',
                                      validators=[validators.optional('Please enter your upline phone number.')])
    password = PasswordField(label='Password',
                             validators=[validators.required('Please enter your password.')])
    password_c = PasswordField(label='Confirm Password',
                               validators=[validators.DataRequired('Please enter your password again.')])
    submit = SubmitField(label='Register',
                         validators=[validators.DataRequired()])


class LoginForm(Form):
    phone_number = StringField(label='Phone Number',
                               validators=[validators.DataRequired('Please enter your phone number.')])
    password = PasswordField(label='Password',
                             validators=[validators.DataRequired('Please enter your password.')])

    submit = SubmitField(label='Log in',
                         validators=[validators.DataRequired()])


class ChangePasswordForm(Form):
    current_password = PasswordField(label='Current Password',
                                     validators=[validators.optional()])
    new_password = PasswordField(label='New Password',
                                 validators=[validators.optional()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[validators.optional()])
    submit = SubmitField(label='Change Password',
                         validators=[validators.DataRequired()])


class ProfileForm(Form):
    name = StringField(label='Name', validators=[validators.optional()])
    family_name = StringField(label='Family Name', validators=[validators.optional()])
    email = StringField('Email',
                        validators=[validators.optional(),
                                    validators.Length(1, 120),
                                    validators.Email()])
    gender = SelectField(label='Gender', validators=[validators.optional()],
                         choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    company = SelectField(label='Company', validators=[validators.optional()],
                          choices=[('Nioshanik', 'Nioshanik'),
                                   ('Panbe riz', 'Panbe riz')])
    birthday_day = StringField(label='Birthday', validators=[validators.optional()])
    bio = TextAreaField(label='Bio', validators=[validators.optional()])
    submit = SubmitField('Save', validators=[validators.DataRequired()])
