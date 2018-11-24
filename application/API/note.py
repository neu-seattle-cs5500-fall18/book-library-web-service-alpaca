from flask import Blueprint, request, jsonify
from application import db
from application.models.note_model import Note
import json
import time

note_bp = Blueprint('note', __name__)

@note_bp.route('/add_note', methods=['POST'])
def add_note():
    args = json.loads(request.get_data())  # get post args and trans to json format
    try:
        book_id = args['book_id']
        user_id = args['user_id']
        content = args['content']
    except:
        return jsonify({
            'message': 'invalid input arguments!'
        }), 400

    if book_id is None or user_id is None or content is None:
        return jsonify({
            'message': 'invalid input arguments!'
        }), 400

    created_at = time.strftime('%Y/%m/%d', time.localtime())
    note = Note(book_id, user_id, content, created_at)
    db.session.add(note)
    db.session.commit()
    return jsonify({
        'message': 'note added'
    }), 201

@note_bp.route('/delete_note', methods=['DELETE'])
def delete_note():
    args = json.loads(request.get_data())
    try:
        note_id = args['note_id']
    except:
        return jsonify({
            'message': 'invalid input argument'
        }),400

    try:
        note_to_delete = db.session.query(Note).filter_by(id=note_id).first()
    except:
        return jsonify({
            'message': 'no such note to delete'
        }),401
    if note_to_delete is None:
        return jsonify({
            'message': 'no such note to delete'
        }), 401

    db.session.delete(note_to_delete)
    db.session.commit()
    return jsonify({
        'message': 'Note deleted'
    }), 200


@note_bp.route('/update_note', methods=['PUT'])
def update_note():
    try:
        note_id = request.args.get('note_id')
    except:
        return jsonify({
            'message':'Get arg failed'
        }),400

    if note_id is None:
        return jsonify({
            'message': 'Did not pass in a note_id'
        }), 400

    try:
        note = db.session.query(Note).filter(Note.id == note_id).first()
    except:
        return jsonify({
            'message': 'No such book to update'
        }), 400
    if note is None:
        return jsonify({
            'message': 'No such note to update'
        }), 400

    book_id = request.args.get('book_id')
    user_id = request.args.get('user_id')
    content = request.args.get('content')
    created_at = time.strftime('%Y/%m/%d', time.localtime())

    if book_id is not None:
        note.book_id = book_id

    if user_id is not None:
        note.user_id = user_id

    if content is not None:
        note.content = content

    if created_at is not None:
        note.created_at = created_at

    db.session.commit()
    return jsonify({
        'message': 'Note updated'
    }), 200


@note_bp.route('/search_note', methods=['GET'])
def search_note():
    note_id = request.args.get('note_id')
    book_id = request.args.get('book_id')
    user_id = request.args.get('user_id')
    conditions = []
    if note_id is not None:  # if book_id given,should only need 1 condition for the query
        conditions.append(Note.id == note_id)
    else:
        if book_id is not None:
            conditions.append(Note.book_id == book_id)

        if user_id is not None:
            conditions.append(Note.user_id == user_id)

    notes = db.session.query(Note).filter(*conditions).all()
    notes = [{'id': note.id, 'book_id': note.book_id, 'user_id': note.user_id, 'content': note.content, 'created_at': note.created_at} for
             note in notes]
    return jsonify({
        'message': 'Query successful',
        'notes': notes
    }), 200