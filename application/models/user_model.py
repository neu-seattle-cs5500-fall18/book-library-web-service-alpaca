from application import db

class User(db.Model):

    __tablename__ = 'libraryuser'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32), unique=False, nullable=False)
    email = db.Column(db.String(255), unique=False, nullable=True)

    def __init__(self, user_name, password, email=''):
        self.user_name = user_name
        self.password = password
        self.email = email

    @property
    def serialize(self):
        return {
            'id': self.book_list_id,
            'name': self.book_list_name,
            'user_name': self.user_name
        }


