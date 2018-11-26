from application import app
from flask_restplus import Api
from application.API.booklist import book_list_apis
from application.API.book import book_apis
from application.API.note import note_apis
from application.API.loan import loan_apis

# init API
book_library_service_api = Api(
    title='Book Library Service API',
    version='1.0',
    description='Book Library Service APIs developed by Team Alpaca.',
)

# add individual namespaces to the API
book_library_service_api.add_namespace(ns=book_list_apis, path='/booklist')
book_library_service_api.add_namespace(ns=book_apis, path='/book')
book_library_service_api.add_namespace(ns=note_apis, path='/note')
book_library_service_api.add_namespace(ns=loan_apis, path='/loan')

# combine the application with the API
book_library_service_api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)