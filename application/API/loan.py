from flask_restplus import Namespace, Resource, reqparse
from application import db
from application.models.loan_model import Loan
from application.models.book_model import Book
from application.models.user_model import User


loan_apis = Namespace('Loan APIs', description='Loan APIs')

parser = reqparse.RequestParser()
parser.add_argument('loan_id', help='loan id')
parser.add_argument('user_id', help='user id')
parser.add_argument('book_id', help='book id')
parser.add_argument('due', help='due')
parser.add_argument('return_date', help='return date')
parser.add_argument('returned', help='1 is returned and 0 is not returned')

@loan_apis.route('/')
class LoanDao(Resource):
    @loan_apis.doc(responses={200: 'Success', 404: 'No matching note'})
    @loan_apis.doc(params={'loan_id': 'loan id'})
    @loan_apis.doc(params={'user_id': 'user id'})
    @loan_apis.doc(params={'book_id': 'book id'})
    @loan_apis.doc(params={'due': 'due'})
    @loan_apis.doc(params={'return_date': 'return date'})
    @loan_apis.doc(params={'returned': '1 is returned and 0 is NOT returned'})
    @loan_apis.doc('get loan info')
    def get(self):
        '''Get the info of a loan.'''
        args = parser.parse_args()
        loan_id = args['loan_id']
        user_id = args['user_id']
        book_id = args['book_id']
        due = args['due']
        return_date = args['return_date']
        returned = args['returned']
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
                conditions.append(Loan.return_date == return_date)

            if returned is not None:
                conditions.append(Loan.returned == returned)
        try:
            loans = db.session.query(Loan).filter(*conditions).all()
        except:
            return {
                'message': 'No Matching Loans'
            }, 404
        if not loans:
            return {
                'message': 'No Matching Loans'
            }, 404

        loans = [{'loan_id': loan.id, 'user_id': loan.user_id, 'book_id': loan.book_id, 'due': str(loan.due),\
                  'return_date': str(loan.return_date), 'returned': loan.returned} for
                 loan in loans]
        return {
            'message': 'Query successful',
            'loans': loans
        }, 200

    @loan_apis.doc(responses={200: 'Success', 400: 'Syntax error', 403: 'Forbid to delete not returned loan', 404: 'No such loan'})
    @loan_apis.doc(params={'loan_id': 'loan id'})
    @loan_apis.doc('Delete loan')
    def delete(self):
        '''Delete a loan by loan_id'''
        args = parser.parse_args()
        try:
            loan_id = args['loan_id']
        except:
            return {
                'message': 'Did not give loan_id'
            }, 400
        if loan_id is None:
            return {
                'message': 'Did not give loan_id'
            }, 400

        try:
            loan_to_delete = db.session.query(Loan).filter(Loan.id == loan_id).first()
        except:
            return {
                'message': 'no such loan to delete'
            }, 404

        if loan_to_delete is None:
            return {
                 'message': 'no such loan to delete'
            }, 404

        if loan_to_delete.returned == 0:
            return {
                'message': 'Can not delete a loan that has not been returned'
            }, 403

        db.session.query(Loan).filter(Loan.id == loan_id).delete()
        db.session.commit()
        return {
            'message': 'Loan deleted'
        }, 200

    @loan_apis.doc(responses={201: 'Loan created', 400: 'Syntax error', 403: 'Forbid to borrow an unavailable book', 404: 'No such user or book'})
    @loan_apis.doc(params={'user_id': 'user id'})
    @loan_apis.doc(params={'book_id': 'book id'})
    @loan_apis.doc(params={'due': 'due'})
    @loan_apis.doc('Loan a book')
    def post(self):
        '''Loan a book'''
        args = parser.parse_args()
        try:
            user_id = args['user_id']
            book_id = args['book_id']
            due = args['due']
        except:
            return {
            'message': 'At least 1 argument is not provided'
        }, 400

        if user_id is None or book_id is None or due is None:
            return {
            'message': 'At least 1 argument is not provided'
        }, 400

        try:
            user = db.session.query(User).filter(User.id == user_id).first()
        except:
            return {
                'message': 'No such user'
            }, 404

        if user is None:
            return {
                'message': 'No such user'
            }, 404
        try:
            book = db.session.query(Book).filter(Book.id == book_id).first()
        except:
            return {
                'message': 'No such book to loan'
            }, 404

        if book is None:
            return {
                'message': 'No such book to loan'
            }, 404

        if book.available == 0:
            return {
                'message': 'This book is not available'
            }, 403

        book.available = 0  # mark book as loaned out
        loan = Loan(user_id, book_id, due)
        db.session.add(loan)
        db.session.commit()
        return {
            'message': 'Loan created'
        }, 201

    @loan_apis.doc(responses={200: 'Success', 400: 'Syntax error', 404: 'No such loan or book'})
    @loan_apis.doc(params={'loan_id': 'loan id'})
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

        due = args['due']
        return_date = args['return_date']

        try:
            loan = db.session.query(Loan).filter(Loan.id == loan_id).first()
        except:
            return {
                'message': 'No such loan to update'
            }, 404
        if loan is None:
            return {
                'message': 'No such loan to update'
            }, 404

        if due is not None:
            loan.due = due

        if return_date is not None:
            book_id = loan.book_id
            try:
                book = db.session.query(Book).filter(Book.id == book_id).first()
            except:
                return {
                    'message': 'Loaned book was deleted'
                }, 404
            if book is None:
                return {
                    'message': 'Loaned book was deleted'
                }, 404
            loan.return_date = return_date
            loan.returned = 1
            book.available = 1  # mark book as returned

        db.session.commit()
        return {
            'message': 'loan updated'
        }, 200
