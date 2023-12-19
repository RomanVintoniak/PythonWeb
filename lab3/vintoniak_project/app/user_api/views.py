from flask import request
from flask_restful import Resource
from app.authentication.models import User
from app.user_api.schemas import UserSchema
from app import db


class UsersApi(Resource):
    
    def get(self):
        users = User.query.all()
        schema = UserSchema(many=True, exclude=('password',))
        return {"users": schema.dump(users)}
    
    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)
        
        db.session.add(user)
        db.session.commit()

        return {"user": schema.dump(user)}, 201


class UserApi(Resource):
    
    def get(self, id):
        schema = UserSchema(exclude=('password',))
        user = User.query.filter_by(id=id).first_or_404()
        
        return {"user": schema.dump(user)}

    def put(self, id):
        schema = UserSchema(partial=True)
        user = User.query.filter_by(id=id).first_or_404()
        
        user = schema.load(request.json, instance=user)
        
        db.session.add(user)
        db.session.commit()
        
        return {"user": schema.dump(user)}
        
    def delete(self, id):
        user = User.query.filter_by(id=id).first_or_404()
        
        db.session.delete(user)
        db.session.commit()
        
        return {"message": f"User {user.username} deleted"}