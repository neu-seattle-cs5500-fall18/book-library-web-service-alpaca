from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Book(db.Model):

    book_id = db.Column(db.String, primary_key=True)
    book_author = db.Column(db.String, nullable=False)
    book_title = db.Column(db.String, nullable=False)
    book_year = db.Column(db.Integer, nullable=False)
    book_genre = db.Column(db.String, nullable=False)
    book_note = db.Column()

    @property
    def serialize(self):
        return {
            'id': self.book_id,
            'author': self.book_author,
            'title': self.book_title,
            'year': self.book_year,
            'genre': self.book_genre
        }

class BookToNotes(db.Model):

    id = db.Column(db.String, primary_key=True)
    book_id = db.Column(db.String, nullable=False)
    note_id = db.Column(db.String, nullable=False)

    @property
    def serialize(self):
        return {
        'id':self.id,
        'book_id':self.book_id,
        'note_id':self.note_id
        }
    