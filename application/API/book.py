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
    book_id = request.args.get('book_id')
    book_author = request.args.get('author')
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')
    book_title = request.args.get('title')
    book_genre = request.args.get('genre')

    conditions = []
    if book_id is not None:   # if book_id given,should only need 1 condition for the query
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

    books = db.session.query(Book).filter(*conditions).all()
    books = [{'id': book.id, 'author': book.author, 'title': book.title, 'year': book.year, 'genre': book.genre} for book in books]
    return jsonify({
        'message': 'Query successful',
        'books': books
    }), 200

@book_bp.route('/update_book', methods=['PUT'])
def update_book():
    try:
        book_id = request.args.get('id')
    except:
        return jsonify({
            'message':'Get arg failed'
        }),400

    book_author = request.args.get('author')
    book_year = request.args.get('year')
    book_title = request.args.get('title')
    book_genre = request.args.get('genre')

    if book_id is None:
        return jsonify({
            'message': 'Did not pass in a book_id'
        }), 400

    try:
        book = db.session.query(Book).filter(Book.id == book_id).first()
    except:
        return jsonify({
            'message': 'No such book to update'
        }), 400
    if book is None:
        return jsonify({
            'message': 'No such book to update'
        }), 400

    if book_author is not None:
        book.author = book_author

    if book_year is not None:
        book.year = book_year

    if book_title is not None:
        book.title = book_title

    if book_genre is not None:
        book.genre = book_genre

    db.session.commit()
    return jsonify({
        'message': 'Book updated'
    }), 200
