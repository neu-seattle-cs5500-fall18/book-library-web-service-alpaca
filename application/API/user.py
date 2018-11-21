from flask import Blueprint
from application import db

user_bp = Blueprint('user', __name__)

@user_bp.route("/user")
def func():
    pass