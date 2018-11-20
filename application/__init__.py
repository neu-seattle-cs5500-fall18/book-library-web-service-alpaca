from application.API.book import book_bp
from application.API.booklist import book_list_bp
from application.API.loan import loan_bp
from application.API.user import user_bp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://iltlntsqhnuuiu:b450237a15174db6eddf51d8af1e8fc1a8eb71509c6277560f04c1c876c4542c@ec2-54-163-230-178.compute-1.amazonaws.com:5432/dhdp0qr21t6ev'

db = SQLAlchemy(app)
# register blueprints for different resources
app.register_blueprint(book_bp)
app.register_blueprint(book_list_bp)
app.register_blueprint(loan_bp)
app.register_blueprint(user_bp)