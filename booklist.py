from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BookList(db.Model):

    book_list_id = db.Column(db.Integer, primary_key=True)
    book_list_name = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String(80), unique=False, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.book_list_id,
            'name': self.book_list_name,
            'user_name': self.user_name
        }

class BookListToBook(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_list_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'list_id': self.book_list_id,
            'book_id': self.book_id
        }