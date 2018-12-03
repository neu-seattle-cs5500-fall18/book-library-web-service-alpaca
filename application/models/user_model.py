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
            'user_id': self.id,
            'user_name': self.user_name,
            'email': self.email
        }


