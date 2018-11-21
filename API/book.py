from flask import Blueprint
from application import db
from application.models.book_model import Book

book_bp = Blueprint('book', __name__)

@book_bp.route("/add_book", methods=['POST'])
def add_book():
	book_id = request.args.get("id")
	book_author = request.args.get("author")
	book_title = request.args.get("title")
	book_year = request.args.get("releaseYear")
	book_genre = request.args.get("genre")
	data = (book_id,book_author,book_title,book_year,book_genre)
	insert_stmt = "INSERT INTO book (id,author,title,year,genre) VALUES (%s,%s,%s,%s,%s);"
	connection = engine.connect()
	connection.execute(insert_stmt,data)
	connection.close()
    return "initial commit AnranBookBranch"

@book_bp.route("/search_book", methods=['GET'])
def search_book():
 	return "search book"


@book_bp.route("/update_book", methods=['PUT'])
def update_book():
	return "update book"

@book.bp.route("/delete_book", methods=['DELETE'])
def delete_book():
	return "delete book"



