from flask_wtf import FlaskForm
from .models import User
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from flask_wtf.file import FileField, FileAllowed 
from flask_login import current_user

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired("This field is required"), Email("Please enter your email address")])
    password = PasswordField("Password", validators=[DataRequired("This field is required"), Length(min=4, max=10)])
    rememberMe = BooleanField("Remember me")
    submit = SubmitField("Log in")
    
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("This field is required"), 
                                                   Length(min=4, max=10),
                                                   Regexp('^[A-Za-z][a-zA-Z0-9._]+$', 0,
                                                            "username must have only letters, numbers, dots or underscores")])
    email = EmailField("Email", validators=[DataRequired("This field is required"), Email("Please enter your email address")])
    password = PasswordField("Password", validators=[DataRequired("This field is required"), Length(min=6)])
    confirmPassword = PasswordField("Confirm password", validators=[DataRequired("This field is required"), EqualTo("password", "Passwords do not match")])
    submit = SubmitField("Sign up")
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already in use")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Enter old password", validators=[DataRequired("This field is required"), 
                                                               Length(min=4, max=10)])
    
    newPassword = PasswordField("Enter new password", validators=[DataRequired("This field is required"), 
                                                                  Length(min=4, max=10)])
    
    confirmNewPassword = PasswordField("Confirm new password", validators=[DataRequired("This field is required"), 
                                                                               Length(min=4, max=10),
                                                                               EqualTo("newPassword", "Passwords do not match")])
    submit = SubmitField("Reset")
    
    def validate_password(self, field):
        if not current_user.checkPassword(field.data):
            raise ValidationError("Incorrect password")
            
            
    
class AddTodoItemForm(FlaskForm):
    title = StringField("Enter a task here", validators=[DataRequired("This field is required")])
    description = StringField("Enter description here", validators=[DataRequired("This field is required")])
    submit = SubmitField("Save")
    
class AddReview(FlaskForm):
    username = StringField("Enter username", validators=[DataRequired("This field is required")])
    email = StringField("Enter email", validators=[DataRequired("This field is required")])
    content = TextAreaField("Eenter content", validators=[DataRequired("This field is required")])
    submit = SubmitField("Add")
    
    
class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[Length(min=4, max=10),
                                                   Regexp('^[A-Za-z][a-zA-Z0-9._]+$', 0,
                                                            "username must have only letters, numbers, dots or underscores")])
    email = EmailField("Email", validators=[Email("Please enter your email address")])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    aboutMe = TextAreaField("About Me")
    submit = SubmitField("Update")
    
    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError('Username already in use')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('Email already registered')