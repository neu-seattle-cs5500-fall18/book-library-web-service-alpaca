from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):

    BookId = db.Column(db.String, primary_key=True)
    BookAuthor = db.Column(db.String, nullable=False)
    BookTitle = db.Column(db.String, nullable=False)
    BookYear = db.Column(db.Integer, nullable=False)
    BookGenre = db.Column(db.String, nullable=False)

    @property
    def serialize(self):
        return {
            'BookId': self.BookId,
            'BookAuthor': self.BookAuthor,
            'BookTitle': self.BookTitle,
            'BookYear': self.BookYear,
            'BookGenre': self.BookGenre
        }
    