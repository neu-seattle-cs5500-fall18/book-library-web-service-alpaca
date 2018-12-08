from application import db
from application.models.user_model import User
from application.models.loan_model import Loan
from flask_restplus import Namespace, Resource, reqparse
import time


user_alert_apis = Namespace('User Alert API', description='User Alert API')
parser = reqparse.RequestParser()
parser.add_argument('user_id', help='user id')
@user_alert_apis.route('/')
class UserAlert(Resource):
    @user_alert_apis.doc(responses={200: 'Success', 400: 'Error'})
    @user_alert_apis.doc('Return list of users who needs to return the loaned books')
    def get(self):
        curr_time = time.strftime("%Y-%m-%d", time.localtime())
        loan_list = db.session.query(Loan)\
                    .filter(Loan.due <= curr_time)\
                    .filter(Loan.returned == 0).all()
        user_id_list = [loan.user_id for loan in loan_list]

        return {
            'message': 'List of users who are required to return their loaned books!',
            'user_id_list': user_id_list
        }

    def post(self):
        args = parser.parse_args()
        try:
            user_id = args['user_id']
        except:
            return {
                'message':'Please provide the user_id!'
            }, 400
        if user_id is None:
            return {
                'message':'Please provide the user_id!'
            }, 400
        curr_time = time.strftime("%Y-%m-%d", time.localtime())
        loan = db.session.quer(Loan).filter(Loan.user_id == user_id)\
                                        .filter(Loan.due<=curr_time).all()
        book_ids = [loan.book_id for loan in loan]
        if len(book_ids) > 0:
            return {
                'message': 'This user need to return his loaned book that passed the due already!',
                'book_ids': book_ids
            }, 200
        else:
            return {
                'message': 'This user has returned all loaned books in time!'
            }, 200

