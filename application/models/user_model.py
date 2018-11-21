from application import db

class User(db.Model):

    __tablename__ = 'libraryuser'

    UserId = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(80), unique=True, nullable=False)
    PassWord = db.Column(db.String(80), unique=False, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.book_list_id,
            'name': self.book_list_name,
            'user_name': self.user_name
        }

