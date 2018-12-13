from application import db
from application.models.user_model import User
from application.models.loan_model import Loan
from application.models.book_model import Book
from flask_restplus import Namespace, Resource, reqparse
import time
import sendgrid
import os
from sendgrid.helpers.mail import *


user_alert_apis = Namespace('User Alert API', description='User Alert API')
parser = reqparse.RequestParser()
parser.add_argument('user_id', help='user id')
@user_alert_apis.route('/')
class UserAlert(Resource):
    @user_alert_apis.doc(responses={200: 'Success'})
    @user_alert_apis.doc('Return list of users who needs to return the loaned books')
    def get(self):
        '''Return a list of users who need to return the loaned books'''
        curr_time = time.strftime("%Y-%m-%d", time.localtime())
        loan_list = db.session.query(Loan)\
                    .filter(Loan.due <= curr_time)\
                    .filter(Loan.returned == 0).all()
        user_id_list = [loan.user_id for loan in loan_list]

        return {
            'message': 'List of users who are required to return their loaned books!',
            'user_id_list': user_id_list
        }, 200

    @user_alert_apis.doc(responses={200: 'Success', 204: 'No books to return', 400: 'Syntax Error'})
    @user_alert_apis.doc(params={'user_id': 'user id'})
    @user_alert_apis.doc('Return list of loaned books that pass the due based on specific user_id. Send email alert to user')
    def post(self):
        '''Returns list of books that need to be returned by input user_id and sends reminder email to that user'''
        args = parser.parse_args()
        try:
            user_id = args['user_id']
        except:
            return {
                'message': 'Please provide the user_id!'
            }, 400
        if user_id is None:
            return {
                'message': 'Please provide the user_id!'
            }, 400
        curr_time = time.strftime("%Y-%m-%d", time.localtime())
        to_send_user = db.session.query(User).filter(User.id == user_id).first()
        raws = db.session.query(Loan, Book).join(Book, Loan.book_id == Book.id)\
                                        .filter(Loan.user_id == user_id)\
                                        .filter(Loan.returned == 0)\
                                        .filter(Loan.due<=curr_time).all()

        book_ids = [raw[0].book_id for raw in raws]
        titles = [raw[1].title for raw in raws]
        str_title = ','.join(titles)

        if len(book_ids) > 0:
            sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
            from_email = Email("alpaca_library_services@alpaca.com")
            to_email = Email(to_send_user.email)
            subject = "(DO NOT REPLY) Reminder: Your loaned books need to be returned immediately"
            content = Content("text/plain", "Dear Customer,"+"\n"+
                                            "Please return the following books:"+"\n"+"\n"
                              + str_title +"\n"+"\n"+"\n"+"\n"+"\n"+"\n"
                              "Best Regards, "+"\n"+"\n"+
                              "Alpaca Library Service")
            mail = Mail(from_email, subject, to_email, content)
            response = sg.client.mail.send.post(request_body=mail.get())
            print(response.status_code)
            print(response.body)
            print(response.headers)

            return {
                'message': 'This user need to return his loaned books that passed the due already! Email alert has been sent to him',
                'book_ids': book_ids
            }, 200
        else:
            return {
                'message': 'This user has returned all loaned books in time!'
            }, 204

