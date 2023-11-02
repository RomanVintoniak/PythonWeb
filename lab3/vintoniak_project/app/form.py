from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("This field is required")])
    password = PasswordField("Password", validators=[DataRequired("This field is required"), Length(min=4, max=10)])
    rememberMe = BooleanField("Remember me")
    submit = SubmitField("Log in")

class ChangePasswordForm(FlaskForm):
    password = PasswordField("Enter new password", validators=[DataRequired("This field is required"), Length(min=4, max=10)])
    repassword = PasswordField("Enter new password again", validators=[DataRequired("This field is required"), Length(min=4, max=10)])
    submit = SubmitField("Change")
    
class AddTodoItemForm(FlaskForm):
    title = StringField("Enter a task here", validators=[DataRequired("This field is required")])
    description = StringField("Enter description here", validators=[DataRequired("This field is required")])
    submit = SubmitField("Save")
    
class AddReview(FlaskForm):
    username = StringField("Enter username", validators=[DataRequired("This field is required")])
    email = StringField("Enter email", validators=[DataRequired("This field is required")])
    content = TextAreaField("Eenter content", validators=[DataRequired("This field is required")])
    submit = SubmitField("Add")
    