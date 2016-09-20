from flask_wtf import Form
from wtforms import StringField, TextAreaField, validators, SubmitField, SelectField


class PostForm(Form):

    subject = StringField(label='Subject', validators=[validators.DataRequired("The post subject.")])
    # date = DateField(label='Publish Date', validators=[validators.DataRequired("The post date")])
    content = TextAreaField(label='Post', validators=[validators.DataRequired("The text post.")])
    type_publication = SelectField(label='Type publication',
                                   validators=[validators.DataRequired("For ilk publication choose once.")],
                                   choices=[('public', 'Public'),
                                            ('subsets', 'Only subsets'),
                                            ('uplines', 'Only uplines'),
                                            ('directs', 'Only directs'),
                                            ('upline', 'Just my upline')])

    submit = SubmitField(label='Publish')


class EditForm(Form):

    subject = StringField(label='Subject', validators=[validators.DataRequired("The post subject.")])
    content = TextAreaField(label='Post', validators=[validators.DataRequired("The text post.")])

    submit = SubmitField(label='Edit')

