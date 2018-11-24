from flask import jsonify
from application import db
from application.models.booklist_model import BookList
from application.models.booklist_model import BookListToBook
from application.models.book_model import Book
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
        user_id = args['user_id']
        list_name = args['list_name']

        books = db.session.query(Book) \
            .join(BookListToBook, Book.id == BookListToBook.book_id) \
            .join(BookList, BookList.id == BookListToBook.book_list_id) \
            .filter(BookList.name == list_name) \
            .filter(BookList.user_id == user_id) \
            .all()

        books = [{'author': book.author, 'year': book.year, 'title': book.title, 'genre': book.genre} for book in books]
        return jsonify({
            'message': 'Here are the book ids of the book {}'.format(list_name),
            'books': books
        }), 200

    @book_list_apis.doc(responses={200: 'Success', 400: 'Error'})
    @book_list_apis.doc(params={'user_id': 'user id'})
    @book_list_apis.doc(params={'list_name': 'name of the book list'})
    @book_list_apis.doc('delete a book list')
    def delete(self):
        '''Delete a book list.'''
        args = parser.parse_args()
        user_id = args['user_id']
        list_name = args['list_name']

        db.session.query(BookList) \
            .filter(BookList.user_id == user_id) \
            .filter(BookList.name == list_name) \
            .delete()
        db.session.commit()
        return jsonify({
            'message': 'Delete book list \'{}\' (owned by user id:{}) successfully.'.format(list_name, user_id)
        }), 200

    @book_list_apis.doc(responses={201: 'Success', 401: 'Error'})
    @book_list_apis.doc(params={'user_id': 'user id'})
    @book_list_apis.doc(params={'list_name': 'name of the book list'})
    @book_list_apis.doc(params={'description': 'description of the book list'})
    @book_list_apis.doc('create a book list')
    def post(self):
        '''Create a book list.'''
        args = parser.parse_args()
        user_id = args['user_id']
        list_name = args['list_name']
        description = args['description']

        created_at = time.strftime('%Y/%m/%d', time.localtime())
        book_list = BookList(user_id, list_name, description, created_at)
        db.session.add(book_list)
        db.session.commit()
        return jsonify({
            'message': 'Create book {} successfully.'.format(list_name)
        }), 200

@book_list_apis.route('/books')
class BookListsToBooks(Resource):

    @book_list_apis.doc(responses={201: 'Success', 401: 'Error'})
    @book_list_apis.doc(params={'user_id': 'user id'})
    @book_list_apis.doc(params={'list_name': 'name of the book list'})
    @book_list_apis.doc(params={'book_id': 'book id'})
    @book_list_apis.doc('delete a book from the book list')
    def delete(self):
        '''Delete a book from the book list.'''
        args = parser.parse_args()
        user_id = args['user_id']
        list_name = args['list_name']
        book_id = args['book_id']

        try:
            book_list_id = BookList.query.filter_by(name=list_name).filter_by(user_id=user_id).first().id
        except:
            return jsonify({
                'message': 'No such book!'
            }), 400

        # delete the record from table booklisttobook
        db.session.query(BookListToBook) \
            .filter(BookListToBook.book_list_id == book_list_id) \
            .filter(BookListToBook.book_id == book_id) \
            .delete()
        db.session.commit()
        return jsonify({
            'message': 'Book(id:{}) is deleted from {}'.format(book_id, list_name)
        }), 200

    @book_list_apis.doc(responses={201: 'Success', 401: 'Error'})
    @book_list_apis.doc(params={'user_id': 'user id'})
    @book_list_apis.doc(params={'list_name': 'name of the book list'})
    @book_list_apis.doc(params={'book_id': 'book id'})
    @book_list_apis.doc('add a book to the book list')
    def put(self):
        '''Add a book to the book list.'''
        args = parser.parse_args()
        user_id = args['user_id']
        list_name = args['list_name']
        book_id = args['book_id']

        book_list = db.session.query(BookList) \
            .filter(BookList.user_id == user_id) \
            .filter(BookList.name == list_name) \
            .first()

        record = BookListToBook(book_list.id, book_id)
        db.session.add(record)
        db.session.commit()
        return jsonify({
            'message': 'Add the book(id:{}) to the list \'{}\' successfully.'.format(book_id, list_name)
        }), 200


########################################################################################################
########################################## legacy ######################################################
########################################################################################################
# book_list_bp = Blueprint('book_list', __name__)
#
# @book_list_bp.route('/delete_book_from_list', methods=['POST'])
# def delete_book_from_list():
#     '''
#     Delete a book from the book list given user_id, list_name and book_id.
#     @author: haoxiang.ma
#     '''
#     args = json.loads(request.get_data())  # get post args and trans to json format
#     try:
#         user_id = args['user_id']
#         list_name = args['list_name']
#         book_id = args['book_id']
#     except:
#         return jsonify({
#             'message': 'Please check the arguments!'
#         }), 400
#
#     try:
#         book_list_id = BookList.query.filter_by(name=list_name).filter_by(user_id=user_id).first().id
#     except:
#         return jsonify({
#             'message': 'No such book!'
#         }), 400
#
#     # delete the record from table booklisttobook
#     db.session.query(BookListToBook)\
#         .filter(BookListToBook.book_list_id==book_list_id)\
#         .filter(BookListToBook.book_id==book_id)\
#         .delete()
#     db.session.commit()
#     return jsonify({
#         'message': 'Book(id:{}) is deleted from {}'.format(book_id, list_name)
#     }), 200

# @book_list_bp.route('/add_book_to_list', methods=['PUT'])
# def add_book_to_list():
#     '''
#     Add a book to the book list.
#     @author: haoxiang.ma
#     '''
#     try:
#         # get specific args
#         user_id = request.args.get('user_id')
#         list_name = request.args.get('list_name')
#         book_id = request.args.get('book_id')
#     except:
#         return jsonify({
#             'message': 'Please check the arguments!'
#         }), 400
#
#     book_list = db.session.query(BookList)\
#         .filter(BookList.user_id==user_id)\
#         .filter(BookList.name==list_name)\
#         .first()
#
#     record = BookListToBook(book_list.id, book_id)
#     db.session.add(record)
#     db.session.commit()
#     return jsonify({
#         'message': 'Add the book(id:{}) to the list \'{}\' successfully.'.format(book_id, list_name)
#     }), 200

# @book_list_bp.route('/get_book_list', methods=['GET'])
# def get_book_list():
#     '''
#     Get books from a book list given user_id & book_list_name.
#     @author: haoxiang.ma
#     '''
#     try:
#         # get specific args
#         user_id = request.args.get('user_id')
#         list_name = request.args.get('list_name')
#     except:
#         return jsonify({
#             'message': 'Please check the arguments!'
#         }), 400
#
#     # join three tables together: book, booklisttobook, booklist
#     # to get book info
#     books = db.session.query(Book)\
#         .join(BookListToBook, Book.id==BookListToBook.book_id)\
#         .join(BookList, BookList.id==BookListToBook.book_list_id)\
#         .filter(BookList.name==list_name)\
#         .filter(BookList.user_id==user_id)\
#         .all()
#
#     books = [{'author': book.author, 'year': book.year, 'title': book.title, 'genre': book.genre} for book in books]
#     return jsonify({
#         'message': 'Here are the book ids of the book {}'.format(list_name),
#         'books': books
#     }), 200

# @book_list_bp.route('/delete_book_list', methods=['DELETE'])
# def delete_book_list():
#     '''
#         Delete a book list.
#         @author: haoxiang.ma
#         '''
#     try:
#         # get specific args
#         user_id = request.args.get('user_id')
#         list_name = request.args.get('list_name')
#     except:
#         return jsonify({
#             'message': 'Please check the arguments!'
#         }), 400
#
#     db.session.query(BookList)\
#         .filter(BookList.user_id==user_id)\
#         .filter(BookList.name==list_name)\
#         .delete()
#     db.session.commit()
#     return jsonify({
#         'message': 'Delete book list \'{}\' (owned by user id:{}) successfully.'.format(list_name, user_id)
#     }), 200

# API for creating book list
# @book_list_bp.route('/create_book_list', methods=['POST'])
# def create_book_list():
#     '''
#     Create a book list given user_id, book_list_name and description.
#     @author haoxiang.ma
#     '''
#     args = json.loads(request.get_data())   # get post args and trans to json format
#     try:
#         # get specific args
#         user_id = args['user_id']
#         list_name = args['list_name']
#         description = args['description']
#     except:
#         return jsonify({
#         'message': 'Please check the arguments!'
#     }), 400
#
#     created_at = time.strftime('%Y/%m/%d', time.localtime())
#     book_list = BookList(user_id, list_name, description, created_at)
#     db.session.add(book_list)
#     db.session.commit()
#     return jsonify({
#         'message': 'Create book {} successfully.'.format(list_name)
#     }), 200