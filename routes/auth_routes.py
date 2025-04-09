from flask import Blueprint, jsonify, request
from auth import login, cadastro
from flask_jwt_extended import jwt_required

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['POST'])
def login_route():
    return login()

@auth_routes.route('/cadastro', methods=['POST'])
def cadastro_route():
    return cadastro()
