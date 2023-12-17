from flask import request
from flask_restful import Resource
from app.authentication.models import User
from app.user_api.schemas import UserSchema
from app import db


class UsersApi(Resource):
    
    def get(self):
        users = User.query.all()
        schema = UserSchema(many=True)
        return {"users": schema.dump(users)}
    
    def post(self):
        schema = UserSchema()
        data = schema.load(request.json)
        
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        user = User(username, email, password)

        db.session.add(user)
        db.session.commit()

        return {"user": schema.dump(user)}


class UserApi(Resource):
    
    def get(self, id):
        schema = UserSchema(partial=True)
        user = User.query.filter_by(id=id).first()
        
        if not user:
            return {"message": "User not found"}, 404
        
        return {"user": schema.dump(user)}

    def put(self, id):
        schema = UserSchema()
        user = User.query.filter_by(id=id).first()
        
        user = schema.load(request.json, instance=user)
        
        db.session.add(user)
        db.session.commit()
        
        return {"user": schema.dump(user)}
        
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
       
        if not user:
            return {"message": "User not found"}, 404
        
        db.session.delete(user)
        db.session.commit()
        
        return {"message": f"User {user.username} deleted"}