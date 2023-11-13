from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class AddFeedback(FlaskForm):
    username = StringField("Enter username", validators=[DataRequired("This field is required")])
    email = StringField("Enter email", validators=[DataRequired("This field is required")])
    content = TextAreaField("Eenter content", validators=[DataRequired("This field is required")])
    submit = SubmitField("Add")