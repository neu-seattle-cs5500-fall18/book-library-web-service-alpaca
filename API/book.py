from flask import Blueprint

book_bp = Blueprint('book', __name__)

@book_bp.route("/book")
def func():
    return "initial commit AnranBookBranch"
