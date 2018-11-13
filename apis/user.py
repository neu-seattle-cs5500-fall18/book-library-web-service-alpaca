from flask import request, jsonify
from flask_restplus import Namespace, Resource, reqparse

from models import *

api = Namespace('User', description='Users related operations')

# Add more arguments if needed
parser = reqparse.RequestParser()
parser.add_argument('username', help='The user\'s username')
parser.add_argument('password', help='The user\'s password')


@api.route('/')
class Users(Resource):
    @api.doc('get_users')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def get(self):
        '''Fetch all users'''
        user_list = User.query.order_by(User.UserId).all()

        # returned list of User objects must be serialized
        response = jsonify(Serializer.serialize_list(user_list))
        response.status_code = 200
        return response

    @api.doc('create_user')
    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    @api.expect(parser)
    def post(self):
        '''Create a new user'''
        username = request.args['username']
        password = request.args['password']
        new_user = User(UserName=username,
                        PassWord=password)
        db.session.add(new_user)
        db.session.flush()
        db.session.commit()
        return new_user.serialize(), 201


@api.route('/<user_id>')
@api.param('user_id', 'The user identifier')
@api.response(404, 'User not found')
class UserOfID(Resource):
    @api.doc('get_user')
    @api.doc(responses={
        200: 'Success',
    })
    def get(self, user_id):
        '''Fetch a user given its identifier'''
        return User.query.get_or_404(user_id).serialize(), 200

    @api.doc(responses={
        200: 'Success',
    })
    @api.expect(parser)
    def put(self, user_id):
        '''Update the information of a user given its identifier'''
        user = User.query.get_or_404(user_id)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        if username is not None:
            user.UserName = username
        if password is not None:
            user.PassWord = password
        db.session.commit()
        return user.serialize(), 200

    @api.doc(responses={
        204: 'Deleted',
    })
    def delete(self, user_id):
        '''Delete an user given its identifier'''
        User.query.get_or_404(user_id)
        User.query.filter_by(UserId=user_id).delete()
        db.session.commit()
        return 'Success', 204
