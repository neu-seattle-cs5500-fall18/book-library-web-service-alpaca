from flask_restplus import Namespace, Resource, reqparse
from application import db
from application.models.note_model import Note

import time

note_apis = Namespace('Note APIs',description='Note APIs')

parser = reqparse.RequestParser()
parser.add_argument('note_id', help='note id')
parser.add_argument('book_id', help='book id')
parser.add_argument('user_id', help='user id')
parser.add_argument('content', help='Note content')


@note_apis.route('/')
class NoteDao(Resource):
    @note_apis.doc(responses={200: 'Success', 400: 'Error'})
    @note_apis.doc(params={'note_id': 'note id'})
    @note_apis.doc(params={'book_id': 'book id'})
    @note_apis.doc(params={'user_id': 'user id'})
    @note_apis.doc('get note info')
    def get(self):
        '''Search note by parameters'''
        args = parser.parse_args()
        note_id = args['note_id']
        book_id = args['book_id']
        user_id = args['user_id']
        conditions = []
        if note_id is not None:
            conditions.append(Note.id == note_id)
        else:
            if book_id is not None:
                conditions.append(Note.book_id == book_id)

            if user_id is not None:
                conditions.append(Note.user_id == user_id)
        try:
            notes = db.session.query(Note).filter(*conditions).all()
        except:
            return{
                'message': 'No Matching notes'
            }, 400

        if not notes:
            return {
                'message': 'No Matching notes'
            }, 400

        notes = [{'note_id': note.id, 'book_id': note.book_id, 'user_id': note.user_id, 'content': note.content} for
                 note in notes]
        return {
            'message': 'Query successful',
            'notes': notes
        }, 200


    @note_apis.doc(responses={200: 'Success', 400: 'Error'})
    @note_apis.doc(params={'note_id': 'note id'})
    @note_apis.doc('Delete note')
    def delete(self):
        '''Delete a note by note_id'''
        args = parser.parse_args()
        try:
            note_id = args['note_id']
        except:
            return {
                'message': 'Did not give note_id'
            }, 400

        if note_id is None:
            return {
                'message': 'Did not give note_id'
            }, 400

        try:
            note_to_delete = db.session.query(Note).filter(Note.id == note_id).first()
        except:
            return {
                'message': 'no such note to delete'
            }, 400
        if note_to_delete is None:
            return {
                'message': 'no such note to delete'
            }, 400

        db.session.query(Note).filter(Note.id == note_id).delete()
        db.session.commit()
        return {
            'message': 'Note deleted'
        }, 200

    @note_apis.doc(responses={200: 'Success', 400: 'Error'})
    @note_apis.doc(params={'book_id': 'book id'})
    @note_apis.doc(params={'user_id': 'user id'})
    @note_apis.doc(params={'content': 'Content'})
    @note_apis.doc('Add a note')
    def post(self):
        '''Add a note'''
        args = parser.parse_args()
        try:
            book_id = args['book_id']
            user_id = args['user_id']
            content = args['content']
        except:
            return {
                'message': 'invalid input arguments!'
            }, 400

        if book_id is None or user_id is None or content is None:
            return {
                'message': 'At least 1 argument is not provided'
            }, 400

        created_at = time.strftime('%Y/%m/%d', time.localtime())
        note = Note(book_id, user_id, content, created_at)
        db.session.add(note)
        db.session.commit()
        return {
            'message': 'note added'
        }, 200

    @note_apis.doc(responses={200: 'Success', 400: 'Error'})
    @note_apis.doc(params={'note_id': 'note id'})
    @note_apis.doc(params={'book_id': 'book id'})
    @note_apis.doc(params={'user_id': 'user id'})
    @note_apis.doc(params={'content': 'Content'})
    @note_apis.doc('Update a note')
    def put(self):
        '''Update a note'''
        args = parser.parse_args()
        try:
            note_id = args['note_id']
        except:
            return {
                'message': 'Get arg failed'
            }, 400

        if note_id is None:
            return {
                'message': 'Did not pass in a note_id'
            }, 400
        book_id = args['book_id']
        user_id = args['user_id']
        content = args['content']
        created_at = time.strftime('%Y/%m/%d', time.localtime())

        try:
            note = db.session.query(Note).filter(Note.id == note_id).first()
        except:
            return {
                'message': 'No such book to update'
            }, 400
        if note is None:
            return {
                'message': 'No such note to update'
            }, 400

        if book_id is not None:
            note.book_id = book_id

        if user_id is not None:
            note.user_id = user_id

        if content is not None:
            note.content = content

        note.created_at = created_at

        db.session.commit()
        return {
            'message': 'Note updated'
        }, 200
