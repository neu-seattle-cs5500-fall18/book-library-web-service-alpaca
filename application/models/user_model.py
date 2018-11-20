from flask_sqlalchemy import SQLAlchemy
from application import app

database = SQLAlchemy(app)

class User(database.Model):
    UserId = database.Column(database.Integer, primary_key=True)
    UserName = database.Column(database.String(80), unique=True, nullable=False)
    PassWord = database.Column(database.String(80), unique=False, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.book_list_id,
            'name': self.book_list_name,
            'user_name': self.user_name
        }


