from flask import jsonify, request
from flask_restplus import Namespace, Resource, reqparse

from models import *

api = Namespace('Note', description='Notes related operations')

parser = reqparse.RequestParser()
parser.add_argument('book_id', help='The book_id of the book which owns this note')
parser.add_argument('user_id', help='The user_id of the owner')
parser.add_argument('content', help='The content of the note')


# Post note json format example:
# {
#   "book_id": book_id,
#   "note": string,
# }
@api.route('/')
class Notes(Resource):
    @api.doc('get_notes')
    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
    })
    @api.param('book_id', 'The book_id of the book which owns this note')
    @api.param('user_id', 'The user_id of the owner')
    def get(self):
        '''Fetch all notes given constraints'''
        args = parser.parse_args()
        book_id = args['book_id']
        user_id = args['user_id']

        if book_id is not None and user_id is not None:
            note_list = Note.query.filter_by(BookId=book_id, UserId=user_id).order_by(Note.NoteId).all()
        elif book_id is not None:
            note_list = Note.query.filter_by(BookId=book_id).order_by(Note.NoteId).all()
        elif user_id is not None:
            note_list = Note.query.filter_by(UserId=user_id).order_by(Note.NoteId).all()
        else:
            note_list = Note.query.order_by(Note.NoteId).all()

        # returned list of User objects must be serialized
        response = jsonify(Serializer.serialize_list(note_list))
        response.status_code = 200
        return response

    @api.doc('create_note')
    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error',
    })
    @api.expect(parser)
    def post(self):
        '''Create a new note'''
        book_id = request.args['book_id']
        user_id = request.args['user_id']
        content = request.args['Content']
        new_note = Note(BookId=book_id,
                        UserId=user_id,
                        Content=content)
        db.session.add(new_note)
        db.session.flush()
        db.session.commit()
        return new_note.serialize(), 201


@api.route('/<note_id>')
@api.param('note_id', 'The note identifier')
@api.response(404, 'Note not found')
class NoteOfID(Resource):
    @api.doc('get_note')
    @api.doc(responses={
        200: 'Success',
    })
    def get(self, note_id):
        '''Fetch a note given its identifier'''
        return Note.query.get_or_404(note_id).serialize()

    @api.doc(responses={
        200: 'Success',
    })
    @api.doc(params={'content': 'The note content'})
    def put(self, note_id):
        '''Update the content of a note given its identifier'''
        note = Note.query.get_or_404(note_id)
        args = parser.parse_args()
        content = args['content']
        if content is not None:
            note.Content = content

        print(note.Content)
        print(content)
        db.session.commit()
        return note.serialize(), 200

    @api.doc(responses={
        204: 'Deleted',
    })
    def delete(self, note_id):
        '''Delete a note given its identifier'''
        Note.query.get_or_404(note_id)
        Note.query.filter_by(NoteId=note_id).delete()
        db.session.commit()
        return 'Success', 204
