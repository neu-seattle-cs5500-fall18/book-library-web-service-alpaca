from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BookToNotes(db.Model):

    BookToNoteId = db.Column(db.String, primary_key=True)
    BookId = db.Column(db.String, db.ForeignKey(Book.BookId), nullable=False)
    NoteId = db.Column(db.String, db.ForeignKey(Note.NoteId), nullable=False)

    @property
    def serialize(self):
        return {
        'BookToNoteId':self.BookToNoteId,
        'BookId':self.BookId,
        'NoteId':self.NoteId
        }