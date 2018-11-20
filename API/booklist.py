from flask import Blueprint

book_list_bp = Blueprint('book_list', __name__)

@book_list_bp.route("/book_list")
def func():
    return 'Hello Book List!!!'