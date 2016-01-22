# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint
from anerp.restful import Api, marshal_with, Resource
from anerp.reqparse import RequestParser
from anerp.models.user import User

blueprint = Blueprint('user', __name__, static_folder='static')

api = Api(blueprint)

arguments = {
    'id': {'type': int, 'help': 'The user\'s id'},
    'username': {'help': 'The user\'s username'},
    'email': {'help': 'The user\'s email'},
    'password': {'help': 'The user\'s password'},
    'first_name': {'help': 'The user\'s first name'},
    'last_name': {'help': 'The user\'s last name'}}


patch_parser = RequestParser(arguments=arguments, remove=['id'])

post_parser = patch_parser.copy(
    update={
        'username': {'required': True},
        'email': {'required': True},
        'password': {'required': True}},
    remove=['first_name', 'last_name'])

public_fields = User.marshal_fields(
    'id',
    'username',
    'email',
    'first_name',
    'last_name',
    'created_at')


@api.route('/<int:id>')
class UserApi(Resource):

    # @marshal_with(public_fields)
    def get(self, id):
        return User.query.get_or_404(id)

    def patch(self, id):
        user = User.query.get_or_404(id)
        args = patch_parser.parse_args()
        for key, value in args.items():
            setattr(user, key, value)
        user.update()
        return self.get(id)

    def delete(self, id):
        User.query.get_or_404(id).delete()
        return '', 204


@api.route('/')
class UserList(Resource):

    @marshal_with(public_fields)
    def get(self):
        return User.query.all()

    @marshal_with(public_fields)
    def post(self):
        args = post_parser.parse_args()
        return User.create(**args)
