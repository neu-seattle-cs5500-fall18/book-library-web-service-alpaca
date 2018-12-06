from application import db
class Loan(db.Model):
    __tablename__ = 'loan'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    due = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    returned = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, book_id, due):
            self.user_id = user_id
            self.book_id = book_id
            self.due = due
            self.returned = 0

    @property
    def serialize(self):
            return {
            'loan_id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'due': self.due,
            'return_date': self.return_date,
            'returned': self.returned
    }


