from flask import Flask
from API.book import book_bp
from API.booklist import book_list_bp
from API.loan import loan_bp
from API.user import user_bp

# init application
app = Flask(__name__)

# register blueprints for different resources
app.register_blueprint(book_bp)
app.register_blueprint(book_list_bp)
app.register_blueprint(loan_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    host = 'localhost'
    port = 9000
    app.run(host=host, port=port, debug=True)