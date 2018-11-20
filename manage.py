# from flask import Flask
from application.API.book import book_bp
from application.API.booklist import book_list_bp
from application.API.loan import loan_bp
from application.API.user import user_bp
#
# # init application
# app = Flask(__name__)
#
# # register blueprints for different resources
# app.register_blueprint(book_bp)
# app.register_blueprint(book_list_bp)
# app.register_blueprint(loan_bp)
# app.register_blueprint(user_bp)

from application import app

app.register_blueprint(book_bp)
app.register_blueprint(book_list_bp)
app.register_blueprint(loan_bp)
app.register_blueprint(user_bp)

@app.route('/')
def main_page():
    return 'Main Page!!!'

if __name__ == '__main__':
    host = 'localhost'
    port = 9000
    app.run(host=host, port=port, debug=True)