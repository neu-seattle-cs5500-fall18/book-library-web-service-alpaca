from application import db
from application.models.book_model import Book
from application.models.user_model import User

class Loan(db.Model):

    __tablename__ = 'Loan'

    LoanId = db.Column(db.Integer, primary_key=True)
    BookId = db.Column(db.Integer, db.ForeignKey(Book.BookId), nullable=False)
    BorrowerId = db.Column(db.Integer, db.Foreignkey(User.UserId), nullable=False)
    Due = db.Column(db.DateTime, unique=False, nullable=True)
    ReturnDate = db.Column(db.DateTime, unique=False, nullable=True)

    @property
    def serialize(self):
        res = {
            'LoanId': self.LoanId,
            'BookId': self.BookId,
            'BorrowerId': self.BorrowerId,
            'Due': self.Due._str_(),
            'ReturnDate': self.ReturnDate._str_(),
        }
        return res

