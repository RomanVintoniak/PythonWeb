from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from app.user_api.views import UsersApi, UserApi

users_api = Blueprint('users_api', __name__, url_prefix='/users-api')
api = Api(users_api, errors=users_api.errorhandler)

api.add_resource(UsersApi, '/users')
api.add_resource(UserApi, '/users/<int:id>')

@users_api.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400

@users_api.errorhandler(404)
def handle_not_found_error(e):
    return jsonify({"message": "User not found"}), 404