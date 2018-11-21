from application import db

class Book(db.Model):

    __tablename__ = 'book'

    book_id = db.Column(db.String, primary_key=True)
    book_author = db.Column(db.String,nullable=False)
    book_title = db.Column(db.String, nullable=False)
    book_year = db.Column(db.Integer, nullable=False)
    book_genre = db.Column(db.String,nullable=False)

    def __init__(self, book_author, book_title, book_year, book_genre):
        self.book_author = book_author
        self.book_title = book_title
        self.book_year = book_year
        self.book_genre = book_genre

        
    @property
    def serialize(self):
        return {
            'id': self.book_id,
            'author': self.book_author,
            'title': self.book_title,
            'year': self.book_year,
            'genre': self.book_genre
        }