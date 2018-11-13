from flask_restplus import Namespace, Resource, reqparse

from models import *

api = Namespace('Book List', description='BookLists related operations')

parser = reqparse.RequestParser()

# TODO: the "owner_id" parameter should be removed after logged in user info is saved
parser.add_argument('owner_id', help='id of the user who created the list')
parser.add_argument('list_name', help='name of the list')
parser.add_argument('books', action='append', help='books (represented as book_id) to be included in the list')


@api.route('/')
class Lists(Resource):

    @api.doc('get_lists')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    @api.doc(params={'owner_id': 'user_id of the owner'})
    @api.doc(params={'list_name': 'name of the list'})
    def get(self):
        '''get all lists given constraints'''
        args = parser.parse_args()
        owner_id = args['owner_id']
        list_name = args['list_name']

        queries = []

        if owner_id is not None:
            queries.append(List.OwnerId==owner_id)
        
        if list_name is not None:
            queries.append(List.ListName==list_name)

        book_list = db.session.query(List, ListToBooks, Book)\
            .join(ListToBooks, List.ListId==ListToBooks.ListId)\
            .join(Book, Book.BookId==ListToBooks.BookId)\
            .filter(*queries).all()

        retList = []

        for book in book_list:
            fields = {}

            for field in Serializer.serialize_list(book):
                for k, v in field.items():
                    if (k not in fields):
                        fields[k] = v

            fields['Created'] = str(fields['Created'])
            
            retList.append(fields)

        dict = {}

        for tmpList in retList:
            print(tmpList)
            if tmpList['ListId'] not in dict:
                tmpList['BookId'] = [tmpList['BookId']]
                dict[tmpList['ListId']] = tmpList
            else:
                dict[tmpList['ListId']]['BookId'].append(tmpList['BookId'])
        
        return list(dict.values()), 200

    @api.doc('create_list')
    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    @api.expect(parser)
    def post(self):
        '''create a list'''
        args = parser.parse_args()
        owner_id = args['owner_id']
        list_name = args['list_name']
        books = args['books']
        new_list = List(OwnerId=owner_id, ListName=list_name)
        
        db.session.add(new_list)
        db.session.commit()

        # must be after list being created, otherwise list_id is null
        for book_id in books:
            new_ListToBooks = ListToBooks(ListId=new_list.ListId, BookId=book_id)
            db.session.add(new_ListToBooks)

        db.session.commit()

        return "Success!", 201


@api.route('/<list_id>')
@api.param('list_id', 'The list identifier')
@api.response(404, 'List not found')
class ListOfID(Resource):
    @api.doc(responses={
        200: 'Success',
    })
    @api.doc('get_list')
    def get(self, list_id):
        '''Fetch a list given its identifier'''
        List.query.get_or_404(list_id)
        queries = []
        queries.append(List.ListId==list_id)
        
        book_list = db.session.query(List, ListToBooks, Book)\
            .join(ListToBooks, List.ListId==ListToBooks.ListId)\
            .join(Book, Book.BookId==ListToBooks.BookId)\
            .filter(*queries).all()

        fields = {}
        fields['books'] = []

        # query returns list of books, need to parse the fields of each book
        for book in book_list:
            for field in Serializer.serialize_list(book):
                for k, v in field.items():
                    if (k == 'BookId' and v not in fields['books']):
                        fields['books'].append(v)
                    elif (k not in fields):
                        fields[k] = v
            
            # Serialize the dateTime type 
            fields['Created'] = str(fields['Created'])

        return fields, 200

    @api.doc(responses={
        200: 'Success',
    })
    @api.expect(parser)
    def put(self, list_id):
        '''update a list given its identifier'''
        book_list = List.query.get_or_404(list_id)
        args = parser.parse_args()
        owner_id = args['owner_id']
        list_name = args['list_name']

        if owner_id is not None:
            book_list.OwnerId = owner_id
        if list_name is not None:
            book_list.ListName = list_name

        # for genres or authors or lists, use the map classes
        db.session.commit()

        return {"update list": "success"}, 200

    @api.doc(responses={
        204: 'Deleted',
    })
    def delete(self, list_id):
        '''delete a list given its identifier'''
        List.query.get_or_404(list_id)
        ListToBooks.query.filter_by(ListId=list_id).delete()
        List.query.filter_by(ListId=list_id).delete()
        db.session.commit()
        return 'Success', 204