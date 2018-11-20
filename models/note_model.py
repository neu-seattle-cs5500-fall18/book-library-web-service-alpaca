from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Note(db.Model):
	NoteId = db.Column(db.String, primary_key=True)
	NoteContent = db.Column(db.String, nullable=False)
	BookId = db.Column(db.String, db.ForeignKey(Book.BookId), nullable=False)

	@property
    def serialize(self):
        return {
            'NoteId': self.NoteId,
            'NoteContent': self.NoteContent,
            'BookId': self.BookId
        }