from marshmallow import fields, validate, validates_schema, ValidationError
from app.authentication.models import User
from app import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    username = fields.String(required=True, validate=[validate.Length(min=4)])
    email = fields.String(required=True, validate=[validate.Email()])
    password = fields.String(required=True, validate=[validate.Length(min=6)])
    
    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get('email')
        if User.query.filter_by(email=email).first():
            raise ValidationError(f"Email {email} allready exists")
    
    @validates_schema
    def validate_username(self, data, **kwargs):
        username = data.get('username')
        if User.query.filter_by(username=username).first():
            raise ValidationError(f"Username {username} allready exists")
            
    class Meta:
        model = User
        load_instance = True