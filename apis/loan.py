from flask_restplus import Namespace, Resource, reqparse
from dateutil import parser as datetime_parser
from models import *


api = Namespace('Loan History', description='Loans related operations')

parser = reqparse.RequestParser()
parser.add_argument('book_id', help='The identifier of the book loaned out')
parser.add_argument('borrower_id', help='The user_id of the borrower of the book')
parser.add_argument('due', help='The due date of the book')
parser.add_argument('actual_return_date', help='The actual return date of the book')

post_parser = parser.copy()
post_parser.remove_argument('actual_return_date')
post_parser.replace_argument('book_id', help='The identifier of the book loaned out', required=True)
post_parser.replace_argument('borrower_id', help='The user_id of the borrower of the book', required=True)


@api.route('/')
class Loans(Resource):
    @api.doc('create_loan')
    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error',
        404: 'Book or User Not Found',
    })
    @api.expect(post_parser)
    def post(self):
        '''create a loan'''
        args = post_parser.parse_args()
        book_id = args['book_id']
        book = Book.query.get_or_404(book_id)
        if book.LoanedOut:
            return "The book is already loaned out", 400
        new_loan_history = LoanHistory(BookId=args['book_id'],
                                       BorrowerId=args['borrower_id'])
        due = args['due']
        if due is not None:
            new_loan_history.Due = datetime_parser.parse(due)
        db.session.add(new_loan_history)
        book.LoanedOut = True
        db.session.flush()
        db.session.commit()
        return new_loan_history.serialize(), 201

    @api.doc('get_loan')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    @api.expect(parser)
    def get(self): 
        '''get all loans given constraints'''
        args = parser.parse_args()
        book_id = args['book_id']
        borrower_id = args['borrower_id']
        due = args['due']
        actual_return_date = args['actual_return_date']

        queries = []
        if book_id is not None:
            queries.append(LoanHistory.BookId == book_id)
        if borrower_id is not None:
            queries.append(LoanHistory.BorrowerId == borrower_id)
        if due is not None:
            due = datetime_parser.parse(due)
            queries.append(LoanHistory.Due == due)
        if actual_return_date is not None:
            actual_return_date = datetime_parser.parse(actual_return_date)
            queries.append(LoanHistory.ActualReturnDate == actual_return_date)

        loan_list = db.session.query(LoanHistory).filter(*queries).order_by(LoanHistory.LoanId).all()
        return Serializer.serialize_list(loan_list), 200


@api.route('/<loan_id>')
@api.param('loan_id', 'The loan identifier')
@api.response(404, 'Loan Not Found')
class LoanOfID(Resource):
    @api.doc(responses={
        200: 'Success',
    })
    @api.doc('get_loan')
    def get(self, loan_id):
        '''Fetch a loan given its identifier'''
        loan = LoanHistory.query.get_or_404(loan_id)
        return loan.serialize(), 200

    @api.doc(responses={
        200: 'Success',
    })
    @api.doc(params={'due': 'The due date of the book'})
    @api.doc(params={'actual_return_date': 'The actual return date of the book'})
    @api.expect(parser)
    def put(self, loan_id):
        '''Update the content of a loan given its identifier'''
        loan = LoanHistory.query.get_or_404(loan_id)
        args = parser.parse_args()
        due = args['due']
        actual_return_date = args['actual_return_date']
        if due is not None:
            loan.Due = datetime_parser.parse(due)
        if actual_return_date is not None:
            # TODO: check if return date is < current date
            loan.ActualReturnDate = datetime_parser.parse(actual_return_date)
            book = Book.query.get_or_404(loan.BookId)
            if book.LoanedOut:
                book.LoanedOut = False
        db.session.commit()
        return loan.serialize(), 200

    @api.doc(responses={
        204: 'Deleted',
    })
    def delete(self, loan_id):
        '''Delete a note given its identifier'''
        loan = LoanHistory.query.get_or_404(loan_id)
        book = Book.query.get_or_404(loan.BookId)
        if book.LoanedOut:
            book.LoanedOut = False
        LoanHistory.query.filter_by(LoanId=loan_id).delete()
        db.session.commit()
        return 'Success', 204
