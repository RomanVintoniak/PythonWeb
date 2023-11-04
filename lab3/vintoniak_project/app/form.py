from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired("This field is required"), Email("Please enter your email address")])
    password = PasswordField("Password", validators=[DataRequired("This field is required"), Length(min=4, max=10)])
    rememberMe = BooleanField("Remember me")
    submit = SubmitField("Log in")
    
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("This field is required"), Length(min=4, max=10)])
    email = EmailField("Email", validators=[DataRequired("This field is required"), Email("Please enter your email address")])
    password = PasswordField("Password", validators=[DataRequired("This field is required"), Length(min=6)])
    confirmPassword = PasswordField("Confirm password", validators=[DataRequired("This field is required"), EqualTo("password", "Passwords do not match")])
    submit = SubmitField("Sign up")

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
    