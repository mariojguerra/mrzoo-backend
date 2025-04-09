from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Animal, ImagemAnimal
from datetime import datetime
import uuid

animal_routes = Blueprint('animal_routes', __name__)

@animal_routes.route("/animais", methods=["POST"])
@jwt_required()
def adicionar_animal():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        if not data or not data.get("nome") or not data.get("especie") or not data.get("raca"):
            return jsonify({"message": "Campos obrigatórios estão faltando!"}), 400

        novo_animal = Animal(
            id_animal=data["id_animal"],
            nome=data["nome"],
            especie=data["especie"],
            raca=data["raca"],
            especie_id=data.get("especie_id"),
            raca_id=data.get("raca_id"),
            idade=data.get("idade"),
            descricao=data.get("descricao"),
            imagem_url=data.get("imagem_url"),
            localizacao=data.get("localizacao"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            usuario_id=current_user_id
        )

        db.session.add(novo_animal)
        db.session.commit()

        return jsonify(novo_animal.to_json()), 201

    except Exception as e:
        print(f"Erro ao adicionar animal: {e}")
        return jsonify({"message": "Erro interno no servidor"}), 500


@animal_routes.route("/meus-animais", methods=["GET"])
@jwt_required()
def listar_meus_animais():
    current_user_id = get_jwt_identity()
    meus_animais = Animal.query.filter_by(usuario_id=current_user_id).all()
    return jsonify([animal.to_json() for animal in meus_animais]), 200


@animal_routes.route("/meus-animais/<int:animal_id>", methods=["PUT"])
@jwt_required()
def editar_animal(animal_id):
    current_user_id = get_jwt_identity()
    animal = Animal.query.filter_by(id=animal_id, usuario_id=current_user_id).first()

    if not animal:
        return jsonify({"message": "Animal não encontrado ou não pertence ao usuário!"}), 404

    data = request.get_json()
    animal.id_animal = data.get("id_animal", animal.id_animal)
    animal.nome = data.get("nome", animal.nome)
    animal.especie = data.get("especie", animal.especie)
    animal.raca = data.get("raca", animal.raca)
    animal.idade = data.get("idade", animal.idade)
    animal.descricao = data.get("descricao", animal.descricao)
    animal.imagem_url = data.get("imagem_url", animal.imagem_url)
    animal.longitude = data.get("longitude", animal.longitude)
    animal.latitude = data.get("latitude", animal.latitude)
    animal.localizacao = data.get("localizacao", animal.localizacao)

    db.session.commit()
    return jsonify(animal.to_json()), 200


@animal_routes.route("/meus-animais/<int:animal_id>", methods=["DELETE"])
@jwt_required()
def deletar_animal(animal_id):
    current_user_id = get_jwt_identity()
    animal = Animal.query.filter_by(id=animal_id, usuario_id=current_user_id).first()

    if not animal:
        return jsonify({"message": "Animal não encontrado ou não pertence ao usuário!"}), 404

    db.session.delete(animal)
    db.session.commit()
    return jsonify({"message": "Animal deletado com sucesso!"}), 200
