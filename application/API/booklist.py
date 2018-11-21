from flask import Blueprint, request, jsonify
from application import db
from application.models.booklist_model import BookList
from application.models.booklist_model import BookListToBook

import json
import time

book_list_bp = Blueprint('book_list', __name__)

@book_list_bp.route('/delete_book_from_list', methods=['POST'])
def delete_book_from_list():
    pass

@book_list_bp.route('/add_book_to_list', methods=['PUT'])
def add_book_to_list():
    pass

@book_list_bp.route('/get_book_list', methods=['GET'])
def get_book_list():
    try:
        user_id = request.args.get('user_id')
        list_name = request.args.get('list_name')
    except:
        return jsonify({
            'message': 'Please check the arguments!'
        }), 400

    book_ids = db.session.query(BookListToBook.book_id)\
        .join(BookList, BookListToBook.book_list_id==BookList.id)\
        .filter(BookList.name==list_name)\
        .filter(BookList.user_id==user_id)

    book_ids = [each[0] for each in book_ids]
    return jsonify({
        'message': 'Here are the book ids of the book {}'.format(list_name),
        'book_ids': book_ids
    }), 200


@book_list_bp.route('/delete_book_list', methods=['DELETE'])
def delete_book_list():
    pass

# API for creating book list
@book_list_bp.route('/create_book_list', methods=['POST'])
def create_book_list():
    args = json.loads(request.get_data())   # get post args and trans to json format
    try:
        # get specific args
        user_id = args['user_id']
        list_name = args['list_name']
        description = args['description']
    except:
        return jsonify({
        'message': 'Please check the arguments!'
    }), 400

    created_at = time.strftime('%Y/%m/%d', time.localtime())
    book_list = BookList(user_id, list_name, description, created_at)
    db.session.add(book_list)
    db.session.commit()
    return jsonify({
        'message': 'Create book {} successfully.'.format(list_name)
    }), 200