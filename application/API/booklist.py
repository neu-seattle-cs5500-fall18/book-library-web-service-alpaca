from flask import Blueprint
from application.models.booklist_model import db
from application.models.booklist_model import BookList

book_list_bp = Blueprint('book_list', __name__)

@book_list_bp.route("/book_list")
def func():
    book_list = BookList(1, 'hhh_list', 'hhh', '2018/11/11')
    db.session.add(book_list)
    db.session.commit()
    return 'Hello Book List!!!'
