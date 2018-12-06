from flask_restplus import Namespace, Resource, reqparse
from application import db
from application.models.book_model import Book

book_apis = Namespace('Book APIs', description='Book APIs')

parser = reqparse.RequestParser()
parser.add_argument('book_id', help='book id')
parser.add_argument('book_author', help='book author')
parser.add_argument('book_title', help='book title')
parser.add_argument('book_year', help='publish year of the book')
parser.add_argument('book_genre', help='book genre')
parser.add_argument('start_year', help='Starting publish year of the book')
parser.add_argument('end_year', help='Ending publish year of the book')
parser.add_argument('available', help='1 is available and 0 is unavailable')


@book_apis.route('/')
class BookDao(Resource):
    @book_apis.doc(responses={200: 'Success', 400: 'Error'})
    @book_apis.doc(params={'book_id': 'book id'})
    @book_apis.doc(params={'book_author': 'book author'})
    @book_apis.doc(params={'book_title': 'book title'})
    @book_apis.doc(params={'start_year': 'Starting publish year of the book'})
    @book_apis.doc(params={'end_year': 'Ending publish year of the book'})
    @book_apis.doc(params={'book_genre': 'book genre'})
    @book_apis.doc(params={'available': '1 is available and 0 is NOT available'})
    @book_apis.doc('get book info')
    def get(self):
        '''Search book by parameters'''
        args = parser.parse_args()
        book_id = args['book_id']
        book_author = args['book_author']
        start_year = args['start_year']
        end_year = args['end_year']
        book_title = args['book_title']
        book_genre = args['book_genre']
        available = args['available']
        conditions = []
        if book_id is not None:  # if book_id given,should only need 1 condition for the query
            conditions.append(Book.id == book_id)
        else:
            if book_author is not None:
                conditions.append(Book.author == book_author)

            if start_year is not None:
                conditions.append(Book.year >= start_year)

            if end_year is not None:
                conditions.append(Book.year <= end_year)

            if book_title is not None:
                conditions.append(Book.title == book_title)

            if book_genre is not None:
                conditions.append(Book.genre == book_genre)

            if available is not None:
                conditions.append(Book.available == available)
        try:
            books = db.session.query(Book).filter(*conditions).all()
        except:
            return {
                'message': 'No matching book'
            }, 400

        if not books:
            return {
                'message': 'No matching book'
            }, 400

        books = [{'id': book.id, 'author': book.author, 'title': book.title, 'year': book.year, 'genre': book.genre,\
                  'available': book.available} for
                 book in books]
        return {
            'message': 'Query successful',
            'books': books
        }, 200


    @book_apis.doc(responses={200: 'Success', 400: 'Error'})
    @book_apis.doc(params={'book_id': 'book id'})
    @book_apis.doc('Delete book')
    def delete(self):
        '''Delete a book by book_id'''
        args = parser.parse_args()
        try:
            book_id = args['book_id']
        except:
            return {
                'message': 'Did not give book_id'
            }, 400

        if book_id is None:
            return {
                'message': 'Did not pass in a book_id'
            }, 400

        try:
            book_to_delete = db.session.query(Book).filter(Book.id == book_id).first()
        except:
            return {
                'message': 'no such book to delete'
            }, 400
        if book_to_delete is None:
            return {
                'message': 'no such book to delete'
            }, 400

        db.session.query(Book).filter(Book.id == book_id).delete()
        db.session.commit()
        return {
            'message': 'book deleted'
        }, 200


    @book_apis.doc(responses={200: 'Success', 400: 'Error'})
    @book_apis.doc(params={'book_author': 'book author'})
    @book_apis.doc(params={'book_title': 'book title'})
    @book_apis.doc(params={'book_year': 'book publish year'})
    @book_apis.doc(params={'book_genre': 'book genre'})
    @book_apis.doc('Create a book')
    def post(self):
        '''Add a book'''
        args = parser.parse_args()
        try:
            book_author = args['book_author']
            book_title = args['book_title']
            book_year = args['book_year']
            book_genre = args['book_genre']
        except:
            return {
                'message': 'At least 1 argument is not provided'
            }, 400
        if book_author is None or book_title is None or book_year is None or book_genre is None:
            return {
                'message': 'At least 1 argument is not provided'
            }, 400

        book = Book(book_author, book_title, book_year, book_genre)
        db.session.add(book)
        db.session.commit()
        return {
            'message': 'Book created'
        }, 200

    @book_apis.doc(responses={200: 'Success', 400: 'Error'})
    @book_apis.doc(params={'book_id': 'book id'})
    @book_apis.doc(params={'book_author': 'book author'})
    @book_apis.doc(params={'book_title': 'book title'})
    @book_apis.doc(params={'book_year': 'book publish year'})
    @book_apis.doc(params={'book_genre': 'book genre'})
    @book_apis.doc('Update a book')
    def put(self):
        '''Update a book'''
        args = parser.parse_args()
        try:
            book_id = args['book_id']
        except:
            return {
                'message': 'Get book id failed'
            }, 400

        if book_id is None:
            return {
                'message': 'Did not pass in a book_id'
            }, 400

        book_author = args['book_author']
        book_year = args['book_year']
        book_title = args['book_title']
        book_genre = args['book_genre']

        try:
            book = db.session.query(Book).filter(Book.id == book_id).first()
        except:
            return {
                'message': 'No such book to update'
            }, 400

        if book is None:
            return {
                'message': 'No such book to update'
            }, 400

        if book_author is not None:
            book.author = book_author

        if book_year is not None:
            book.year = book_year

        if book_title is not None:
            book.title = book_title

        if book_genre is not None:
            book.genre = book_genre

        db.session.commit()
        return {
            'message': 'Book updated'
        }, 200
