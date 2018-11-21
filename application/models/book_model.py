from application import db

class Book(db.Model):

    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String,nullable=False)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String,nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.book_id,
            'author': self.book_author,
            'title': self.book_title,
            'year': self.book_year,
            'genre': self.book_genre
        }