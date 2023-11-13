from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddTodoItemForm(FlaskForm):
    title = StringField("Enter a task here", validators=[DataRequired("This field is required")])
    description = StringField("Enter description here", validators=[DataRequired("This field is required")])
    submit = SubmitField("Save")