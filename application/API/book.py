from flask import Blueprint
from application import db
book_bp = Blueprint('book', __name__)

#insert
# db.session.add()
# db.session.commit()


# @book_bp.route("/add_book")
# def add_book():
# 	book_id = request.args.get("id")
# 	book_author = request.args.get("author")
# 	book_title = request.args.get("title")
# 	book_year = request.args.get("releaseYear")
# 	book_genre = request.args.get("genre")
# 	data = (book_id,book_author,book_title,book_year,book_genre)
# 	insert_stmt = "INSERT INTO book (id,author,title,year,genre) VALUES (%s,%s,%s,%s,%s);"
# 	connection = engine.connect()
# 	connection.execute(insert_stmt,data)
# 	connection.close()
# 	return "initial commit AnranBookBranch"