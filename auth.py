# auth.py
from flask_jwt_extended import JWTManager, create_access_token
from flask import request, jsonify
from models import Usuario
from models import db

jwt = JWTManager()

def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Nome de usuário e senha são obrigatórios!'}), 400

    usuario = Usuario.query.filter_by(username=username).first()
    if usuario and usuario.check_password(password):
        # Gerar o token JWT
        access_token = create_access_token(identity=str(usuario.id))

        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Credenciais inválidas!'}), 401

def cadastro():
    try:
        data = request.get_json()

        # Verificar se o corpo da requisição contém os campos obrigatórios
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Nome de usuário e senha são obrigatórios!'}), 400

        username = data.get('username')
        password = data.get('password')

        # Verificar se o nome de usuário já existe
        user_exists = Usuario.query.filter_by(username=username).first()
        if user_exists:
            return jsonify({'message': 'Usuário já existe!'}), 400

        # Criação do novo usuário
        novo_usuario = Usuario(username=username)
        novo_usuario.set_password(password)
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({'message': 'Usuário criado com sucesso!'}), 201
    except Exception as e:
        # Logar o erro detalhado para facilitar o diagnóstico
        print(f"Erro no cadastro: {e}")
        return jsonify({'message': 'Erro interno no servidor!'}), 500
