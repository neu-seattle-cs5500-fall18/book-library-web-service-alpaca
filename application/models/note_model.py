from application import db

class Note(db.Model):

	__tablename__ = 'note'

	note_id = db.Column(db.String, primary_key=True)
	book_id = db.Column(db.String, db.ForeignKey(Book.book_id), nullable=False)
	user_id = db.Column(db.String, db.ForeignKey(user.UserId ), nullable=False)
	content = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.Date, nullable=False)

	def __init__(self, book_id, user_id, content, created_at):
		self.book_id = book_id
		self.user_id = user_id
		self.content = content
		self.created_at = created_at

	@property
    def serialize(self):
        return {
            'note_id': self.note_id,
            'book_id': self.book_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at
        }