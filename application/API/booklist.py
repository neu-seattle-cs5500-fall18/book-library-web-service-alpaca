from application import db
from application.models.booklist_model import BookList
from application.models.booklist_model import BookListToBook
from application.models.book_model import Book
from application.models.user_model import User
from flask_restplus import Namespace, Resource, reqparse

import time

book_list_apis = Namespace('Book List API', description='Book List API')
parser = reqparse.RequestParser()
parser.add_argument('user_id', help='user id')
parser.add_argument('book_id', help='book id')
parser.add_argument('list_name', help='name of the book list')
parser.add_argument('description', help='description of the book list')

@book_list_apis.route('/')
class BookLists(Resource):

    @book_list_apis.doc(responses={200: 'Success', 400: 'Error'})
    @book_list_apis.doc(params={'user_id': 'user id'})
    @book_list_apis.doc(params={'list_name': 'name of the book list'})
    @book_list_apis.doc('get book list info')
    def get(self):
        '''Get the info of a book list.'''
        args = parser.parse_args()
        try:
            user_id = args['user_id']
        except:
            return {
                'message': 'Please provide your user id!'
            }, 400

        try:
            list_name = args['list_name']
        except:
            return {
                'message': 'Please provide the book list name!'
            }, 400

        books = db.session.query(Book) \
            .join(BookListToBook, Book.id == BookListToBook.book_id) \
            .join(BookList, BookList.id == BookListToBook.book_list_id) \
            .filter(BookList.name == list_name) \
            .filter(BookList.user_id == user_id) \
            .all()

        books = [{'author': book.author, 'year': book.year, 'title': book.title, 'genre': book.genre} for book in books]
        return {
            'message': 'Here are the book ids of the book {}'.format(list_name),
            'books': books
        }, 200

    @book_list_apis.doc(responses={200: 'Success', 400: 'Error'})
    @book_list_apis.doc(params={'user_id': 'user id'})
    @book_list_apis.doc(params={'list_name': 'name of the book list'})
    @book_list_apis.doc('delete a book list')
    def delete(self):
        '''Delete a book list.'''
        args = parser.parse_args()
        try:
            user_id = args['user_id']
        except:
            return {
                'message': 'Please provide your user id!'
            }, 400

        try:
            list_name = args['list_name']
        except:
            return {
                'message': 'Please provide the book list name!'
            }, 400

        deleted_row_count = db.session.query(BookList) \
            .filter(BookList.user_id == user_id) \
            .filter(BookList.name == list_name) \
            .delete()
        db.session.commit()

        if deleted_row_count > 0:
            return {
                'message': 'Delete book list \'{}\' (owned by user id:{}) successfully.'.format(list_name, user_id)
            }, 200
        else:
            return {
                'message': 'No such book list!'
            }, 400

    @book_list_apis.doc(responses={201: 'Success', 401: 'Error'})
    @book_list_apis.doc(params={'user_id': 'user id'})
    @book_list_apis.doc(params={'list_name': 'name of the book list'})
    @book_list_apis.doc(params={'description': 'description of the book list'})
    @book_list_apis.doc('create a book list')
    def post(self):
        '''Create a book list.'''
        args = parser.parse_args()
        try:
            user_id = args['user_id']
        except:
            return {
                'message': 'Please provide your user id!'
            }, 401

        try:
            list_name = args['list_name']
        except:
            return {
                'message': 'Please provide the book list name!'
            }, 401

        try:
            description = args['description']
        except:
            return {
                'message': 'Please provide the description of the book list!'
            }, 401

        existed_user = db.session.query(User)\
            .filter(User.id == user_id).all()

        if len(existed_user) == 0:
            return {
                'message': 'There is no such user!'
            }, 401

        existed_book_list = db.session.query(BookList)\
            .filter(BookList.user_id == user_id)\
            .filter(BookList.name == list_name)\
            .all()

        if len(existed_book_list) > 0:
            return {
                'message': 'The book list of the same name already exists!'
            }, 401

        created_at = time.strftime('%Y/%m/%d', time.localtime())
        book_list = BookList(user_id, list_name, description, created_at)
        db.session.add(book_list)
        db.session.commit()
        return {
            'message': 'Create book {} successfully.'.format(list_name)
        }, 201

@book_list_apis.route('/books')
class BookListsToBooks(Resource):

    @book_list_apis.doc(responses={200: 'Success', 400: 'Error'})
    @book_list_apis.doc(params={'user_id': 'user id'})
    @book_list_apis.doc(params={'list_name': 'name of the book list'})
    @book_list_apis.doc(params={'book_id': 'book id'})
    @book_list_apis.doc('delete a book from the book list')
    def delete(self):
        '''Delete a book from the book list.'''
        args = parser.parse_args()
        try:
            user_id = args['user_id']
        except:
            return {
                'message': 'Please provide your user id!'
            }, 400

        try:
            list_name = args['list_name']
        except:
            return {
                'message': 'Please provide the book list name!'
            }, 400

        try:
            book_id = args['book_id']
        except:
            return {
                'message': 'Please provide the book id!'
            }, 400

        try:
            book_list_id = BookList.query.filter_by(name=list_name).filter_by(user_id=user_id).first().id
        except:
            return {
                'message': 'No such book!'
            }, 400

        # delete the record from table booklisttobook
        db.session.query(BookListToBook) \
            .filter(BookListToBook.book_list_id == book_list_id) \
            .filter(BookListToBook.book_id == book_id) \
            .delete()
        db.session.commit()
        return {
            'message': 'Book(id:{}) is deleted from {}'.format(book_id, list_name)
        }, 200

    @book_list_apis.doc(responses={201: 'Success', 401: 'Error'})
    @book_list_apis.doc(params={'user_id': 'user id'})
    @book_list_apis.doc(params={'list_name': 'name of the book list'})
    @book_list_apis.doc(params={'book_id': 'book id'})
    @book_list_apis.doc('add a book to the book list')
    def put(self):
        '''Add a book to the book list.'''
        args = parser.parse_args()
        try:
            user_id = args['user_id']
        except:
            return {
                'message': 'Please provide your user id!'
            }, 400

        try:
            list_name = args['list_name']
        except:
            return {
                'message': 'Please provide the book list name!'
            }, 400

        try:
            book_id = args['book_id']
        except:
            return {
                'message': 'Please provide the book id!'
            }, 400

        book_list = db.session.query(BookList) \
            .filter(BookList.user_id == user_id) \
            .filter(BookList.name == list_name) \
            .first()

        record = BookListToBook(book_list.id, book_id)
        db.session.add(record)
        db.session.commit()
        return {
            'message': 'Add the book(id:{}) to the list \'{}\' successfully.'.format(book_id, list_name)
        }, 200
