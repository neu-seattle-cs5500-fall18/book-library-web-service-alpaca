from flask_restplus import Namespace, Resource, reqparse
from application import db
from application.models.loan_model import Loan

import time

loan_apis = Namespace('Loan APIs', description='Loan APIs')

parser = reqparse.RequestParser()
parser.add_argument('loan_id', help='loan id')
parser.add_argument('user_id', help='user id')
parser.add_argument('book_id', help='book id')
parser.add_argument('due', help='due')
parser.add_argument('return_date', help='return date')

@loan_apis.route('/')
class LoanDao(Resource):

    @loan_apis.doc(responses={200: 'Success', 400: 'Error'})
    @loan_apis.doc(params={'loan_id': 'loan id'})
    @loan_apis.doc(params={'user_id': 'user id'})
    @loan_apis.doc(params={'book_id': 'book id'})
    @loan_apis.doc(params={'due': 'due'})
    @loan_apis.doc(params={'return_date': 'return date'})
    @loan_apis.doc('get loan info')
    def get(self):
        '''Get the info of a loan.'''
        args = parser.parse_args()
        loan_id = args['loan_id']
        user_id = args['user_id']
        book_id = args['book_id']
        due = args['due']
        return_date = args['return date']
        conditions = []
        if loan_id is not None:
            conditions.append(Loan.id == loan_id)
        else:
            if user_id is not None:
                conditions.append(Loan.user_id == user_id)

            if book_id is not None:
                conditions.append(Loan.book_id == book_id)

            if due is not None:
                conditions.append(Loan.due == due)

            if return_date is not None:
                conditions.append(Loan.return_date ==return_date)

        loans = db.session.query(Loan).filter(*conditions).all()
        loans = [{'loan_id': loan_id, 'user_id': loan.user_id, 'book_id': loan.book_id, 'due': loan.due, 'return_date': loan.return_date} \
                 for loan in loans]
        return {
            'message': 'Query successful',
            'loans': loans
        }, 200


    @loan_apis.doc(responses={200: 'Success', 400: 'Error'})
    @loan_apis.doc(params={'loan_id': 'loan id'})
    @loan_apis.doc('Delete loan')
    def delete(self):
        '''Delete a loan by loan_id'''
        args = parser.parse_args()
        try:
            loan_id = args['loan_id']
        except:
            return {
                'message': 'Did not give note_id'
            }, 400

        try:
            loan_to_delete = db.session.query(Loan).filter(Loan.id==loan_id)
        except:
            return {
                'message': 'no such note to delete'
            }, 401
        if loan_to_delete is None:
            return {
                 'message': 'no such note to delete'
            }, 401

        loan_to_delete.delete()
        db.session.commit()
        return {
            'message': 'Note deleted'
        }, 200

    @loan_apis.doc(responses={200: 'Success', 400:'Error'})
    @loan_apis.doc(params={'user_id': 'user id'})
    @loan_apis.doc(params={'book_id': 'book id'})
    @loan_apis.doc(params={'due': 'due'})
    @loan_apis.doc(params={'return_date': 'return date'})
    @loan_apis.doc('Loan a book')
    def post(self):
        '''Loan a book'''
        args = parser.parse_args()
        try:
            user_id = args['user_id']
            book_id = args['book_id']
            due = args['due']
            return_date = args['return_date']
        except:
            return {
            'message': 'invaild input arguments!'
        }, 400

        if user_id is None or book_id is None or due is None or return_date is None:
            return {
            'message': 'At least 1 argument is not provided'
        }, 400

        created_at = time.strftime('%Y/%m/%d', time.localtime())
        loan = Loan(user_id, book_id, due, return_date, created_at)
        db.session.add(loan)
        db.session.commit()
        return {
            'message': 'loan added'
        }, 200

    @loan_apis.doc(responses={200: 'Success', 400:'Error'})
    @loan_apis.doc(params={'loan_id': 'loan id'})
    @loan_apis.doc(params={'user_id': 'user id'})
    @loan_apis.doc(params={'book_id': 'book id'})
    @loan_apis.doc(params={'due': 'due'})
    @loan_apis.doc(params={'return_date': 'return date'})
    @loan_apis.doc('update a loan')
    def put(self):
        '''Update a loan'''
        args = parser.parse_args()
        try:
            loan_id = args['loan_id']
        except:
            return {
                'message': 'Get arg failed'
            }, 400

        if loan_id is None:
            return {
                'message': 'Did not pass in a loan_id'
            }, 400
        user_id = args['user_id']
        book_id = args['book_id']
        due = args['due']
        return_date = args['return_date']
        created_at = time.strftime('%Y/%m/%d', time.localtime())

        try:
            loan = db.session.query(Loan).filter(Loan_id == loan_id).first()
        except:
            return {
                'message': 'No such loan to update'
            }, 400
        if loan is None:
            return {
                'message': 'No such loan to update'
            }, 400

        if user_id is not None:
            loan.user_id = user_id

        if book_id is not None:
            loan.book_id = book_id

        if due is not None:
            loan.due = due

        if return_date is not None:
            loan.return_date = return_date

        loan.created_at = created_at

        db.session.commit()
        return {
            'message': 'loan updated'
        }, 200