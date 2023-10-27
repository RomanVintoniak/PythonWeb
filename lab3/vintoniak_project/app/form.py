from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
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