from application import db
class Loan(db.Model):
    __tablename__ = 'loan'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    due = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    def __init__(self, user_id, book_id, due, return_date, created_at):
            self.user_id = user_id
            self.book_id = book_id
            self.due = due
            self.return_date = return_date
            self.created_at = created_at

    @property
    def serialize(self):
            return {
            'loan_id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'due': self.due,
            'return_date': self.return_date,
            'created_at': self.created_at
    }


