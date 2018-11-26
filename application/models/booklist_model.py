from application import db

class BookList(db.Model):

    __tablename__ = 'booklist'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.Date)

    def __init__(self, user_id, name, description, created_at):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.created_at = created_at

    @property
    def serialize(self):
        return {
            'id': self.book_list_id,
            'name': self.book_list_name,
            'user_id': self.user_id,
            'description': self.description,
            'created_at': self.created_at
        }

class BookListToBook(db.Model):

    __tablename__ = 'booklisttobook'

    id = db.Column(db.Integer, primary_key=True)
    book_list_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)

    def __init__(self, book_list_id, book_id):
        self.book_list_id = book_list_id
        self.book_id = book_id

    @property
    def serialize(self):
        return {
            'id': self.id,
            'list_id': self.book_list_id,
            'book_id': self.book_id
        }