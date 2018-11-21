from flask import Blueprint, request, jsonify
from application import db
from application.models.booklist_model import BookList
import json
import time

book_list_bp = Blueprint('book_list', __name__)

# @book_list_bp.route("/book_list")
# def func():
#     book_list = BookList(1, 'hhh_list', 'hhh', '2018/11/11')
#     db.session.add(book_list)
#     db.session.commit()
#     return 'Hello Book List!!!'

@book_list_bp.route('/delete_book_from_list', methods=['POST'])
def delete_book_from_list():
    pass

@book_list_bp.route('/add_book_to_list', methods=['PUT'])
def add_book_to_list():
    pass

@book_list_bp.route('/get_book_list', methods=['GET'])
def get_book_list():
    pass

@book_list_bp.route('/delete_book_list', methods=['DELETE'])
def delete_book_list():
    pass

@book_list_bp.route('/create_book_list', methods=['POST'])
def create_book_list():
    args = json.loads(request.get_data())
    try:
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