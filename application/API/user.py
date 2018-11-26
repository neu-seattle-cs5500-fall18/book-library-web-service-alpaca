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

        try:
            user = db.session.query(User) \
                .filter(User.name == user_name) \
                .filter(User.password == password) \
                .first()
        except:
            return {
                'message': 'Log in error! Please check your username or password!'
            }, 400

        if user is not None:
            return {
                       'message': 'User \'{}\' logs in successfully.'.format(user_name)
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

        try:
            user_name = db.session.query(User) \
                .filter(User.name == user_name) \
                .first()\
                .name
        except:
            new_user = User(user_name, password, email)
            db.session.add(new_user)
            db.session.commit()
            return {
                       'message': 'User \'{}\' signs up successfully.'.format(user_name)
                   }, 201

        return {
                   'message': 'The user name \'{}\' exists! Please use another name!'.format(user_name)
               }, 401



