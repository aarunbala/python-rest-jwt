import sqlite3
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity
)
from models.user import UserModel



class UserRegister(Resource):
    _user_parser = reqparse.RequestParser()
    _user_parser.add_argument('username',
            type=str,
            required=True,
            help='username cannot be blank')
    _user_parser.add_argument('password',
            type=str,
            required=True,
            help='password cannot be blank')
    _user_parser.add_argument('user_role',
            type=str,
            required=True,
            help='user_role cannot be blank')
    def post(self):
        data = self._user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'Username already taken'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_userid(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_userid(user_id)
        if user:
            user.delete_from_db()
            return {'message': "User {} deleted".format(user.username)}
        return {'message': 'User not found'}, 404

class UserList(Resource):
    @classmethod
    def get(cls):
        return {'users': [user.json() for user in UserModel.find_all()]}

class UserLogin(Resource):
    _user_parser = reqparse.RequestParser()
    _user_parser.add_argument('username',
            type=str,
            required=True,
            help='username cannot be blank')
    _user_parser.add_argument('password',
            type=str,
            required=True,
            help='password cannot be blank')

    @classmethod
    def post(cls):
        data = cls._user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.user_role, fresh=True)
            refresh_token = create_refresh_token(user.user_role)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid Credentials'}, 401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200