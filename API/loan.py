from flask import Blueprint

loan_bp = Blueprint('loan', __name__)

@loan_bp.route("/loan")
def func():
    pass