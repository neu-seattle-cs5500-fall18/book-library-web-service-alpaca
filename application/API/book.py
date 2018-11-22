from flask import Blueprint, request, jsonify
from application import db
from application.models.book_model import Book
import json

book_bp = Blueprint('book', __name__)

@book_bp.route('/add_book', methods=['POST'])
def add_book():
    args = json.loads(request.get_data())  # get post args and trans to json format
    try:
        book_author = args['book_author']
        book_title = args['book_title']
        book_year = args['book_year']
        book_genre = args['book_genre']
        '''
        book_author = "Conan"
        book_title = "Sherlock"
        book_year = 1890
        book_genre = "Mystery"
        '''
    except:
        return jsonify({
            'message': 'invalid input arguments!'
        }), 400

    book = Book(book_author, book_title, book_year, book_genre)
    db.session.add(book)
    db.session.commit()
    return jsonify({
        'message': 'book inserted'
    }), 201


@book_bp.route('/delete_book', methods=['DELETE'])
def delete_book():
    args = json.loads(request.get_data())
    try:
        target_id = args['book_id']
    except:
        return jsonify({
            'message': 'invalid input argument'
        }),400

    try:
        book_to_delete = db.session.query(Book).filter_by(id=target_id).first()
    except:
        return jsonify({
            'message': 'no such book to delete'
        }),401

    db.session.delete(book_to_delete)
    db.session.commit()
    return jsonify({
        'message': 'book deleted'
    }), 200

@book_bp.route('/search_book', methods=['GET'])
def search_book():
    return "this is search book"