from application import db

class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String, nullable=False)

    def __init__(self, book_author, book_title, book_year, book_genre):
        self.author = book_author
        self.title = book_title
        self.year = book_year
        self.genre = book_genre

    @property
    def serialize(self):
        return {
            'id': self.book_id,
            'author': self.author,
            'title': self.title,
            'year': self.year,
            'genre': self.genre
        }