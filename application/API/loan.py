from flask import Blueprint
from application import db

loan_bp = Blueprint('loan', __name__)

@loan_bp.route("/loan")
def func():
    pass