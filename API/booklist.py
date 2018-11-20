from flask import Blueprint
from sqlalchemy import create_engine

book_list_bp = Blueprint('book_list', __name__)

DATABASE_URL = 'postgres://iltlntsqhnuuiu:b450237a15174db6eddf51d8af1e8fc1a8eb71509c6277560f04c1c876c4542c@ec2-54-163-230-178.compute-1.amazonaws.com:5432/dhdp0qr21t6ev'

engine = create_engine(DATABASE_URL, echo=True)

@book_list_bp.route("/book_list")
def func():
    return 'Hello Book List!!!'

@book_list_bp.route('/dummy')
def dummy():
    with engine.connect() as con:
        rs = con.execute('insert into person(name, age) values(\'ggg\', 18)')
        return "Success!"