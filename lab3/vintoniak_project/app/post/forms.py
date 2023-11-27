from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed


class AddUpdatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired("This field is required")])
    text = TextAreaField("Post content")
    image = FileField('Add post image', validators=[FileAllowed(['jpg', 'png'])])
    postType = SelectField("Post type (select one)", choices=[
        ('PUBLICATION', "Publication"), ('NEWS', 'News'), ('MEMES', 'Memes'),
        ('SPORT', 'Sport'), ('OTHER', 'Other')
    ])
    submit = SubmitField("Create post")