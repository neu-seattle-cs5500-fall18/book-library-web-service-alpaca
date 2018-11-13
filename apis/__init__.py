from flask_restplus import Api

from apis.book import api as book_api
from apis.user import api as user_api
from apis.booklist import api as list_api
from apis.loan import api as loan_api
from apis.note import api as note_api

api = Api(
    title='Library API',
    version='1.0',
    description='A simple library API for course CS5500',
)

api.add_namespace(book_api, path='/books')
api.add_namespace(user_api, path='/users')
api.add_namespace(list_api, path='/booklists')
api.add_namespace(loan_api, path='/loans')
api.add_namespace(note_api, path='/notes')
