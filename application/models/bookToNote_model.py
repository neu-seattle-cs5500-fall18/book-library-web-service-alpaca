from application import db

class BookToNote(db.Model):
#这个BookToNote 应该不需要
	__tablename__ = 'booktonote'

    book_to_note_id = db.Column(db.String, primary_key=True)
    book_id = db.Column(db.String, db.ForeignKey(Book.book_id), nullable=False)
    note_id = db.Column(db.String, db.ForeignKey(Note.note_id), nullable=False)

    def __init__(self, book_id, note_id):
    	self.book_id = book_id
    	self.note_id = note_id

    @property
    def serialize(self):
        return {
        'book_to_note_id':self.book_to_note_id,
        'book_id':self.book_id,
        'note_id':self.note_id
        }