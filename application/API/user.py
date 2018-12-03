from application import db
from application.models.user_model import User
from flask_restplus import Namespace, Resource, reqparse

user_apis = Namespace('User API', description='User API')
parser = reqparse.RequestParser()
parser.add_argument('user_name', help='user name')
parser.add_argument('password', help='password')
parser.add_argument('email', help='email address')

@user_apis.route('/')
class Users(Resource):

    @user_apis.doc(responses={200: 'Success', 400: 'Error'})
    @user_apis.doc(params={'user_name': 'user name'})
    @user_apis.doc(params={'password': 'password'})
    @user_apis.doc('log in')
    def get(self):
        '''Sign in.'''
        args = parser.parse_args()
        user_name = args['user_name']
        password = args['password']
        user = db.session.query(User).filter(User.user_name == user_name).first()

        if user is None:
            return {
                'message': 'Sign in error! No such user name!'
            }, 400

        else:
            if password != user.password:
                return {
                    'message': 'Sign in error! Incorrect password!'
                }, 400

            user_id = user.id
            name = user.user_name
            email = user.email
            return {
                'message': 'Sign in successful',
                'user id': user_id,
                'user name': name,
                'user email': email
            }, 200

    @user_apis.doc(responses={201: 'Success', 401: 'Error'})
    @user_apis.doc(params={'user_name': 'user name'})
    @user_apis.doc(params={'password': 'password'})
    @user_apis.doc(params={'email': 'email address'})
    @user_apis.doc('sign up')
    def post(self):
        '''Sign up.'''
        args = parser.parse_args()
        user_name = args['user_name']
        password = args['password']
        email = args['email']

        user = db.session.query(User).filter(User.user_name == user_name).first()
        if user is not None:
            return {
                'message': 'This user name already exists. Please use a different user name'
            }, 401

        new_user = User(user_name, password, email)
        db.session.add(new_user)
        db.session.commit()
        return {
            'message': 'Sign up successful',
            'user id': new_user.id,
            'user name': user_name,
            'user email': email
        }, 201
