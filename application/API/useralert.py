from application import db
from application.models.user_model import User
from application.models.loan_model import Loan
from application.models.book_model import Book

from flask_restplus import Namespace, Resource, reqparse
import time


user_alert_apis = Namespace('User Alert API', description='User Alert API')

@user_alert_apis.route('/')
class UserAlert(Resource):
    @user_alert_apis.doc(responses={200: 'Success', 400: 'Error'})
    @user_alert_apis.doc('Return list of users who needs to return the loaned books')
    def get(self):
        curr_time = time.strftime("%Y-%m-%d", time.localtime())
        user_list = db.session.query(Loan)\
                    .filter(Loan.due <= curr_time)\
                    .filter(Loan.returned == 0).all()
        user_id_list = [user.id for user in user_list]

        return {
            'message': 'List of users who are required to return their loaned books!',
            'user_id_list': user_id_list
        }


