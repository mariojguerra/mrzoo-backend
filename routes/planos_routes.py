from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Plano

planos_routes = Blueprint('planos_routes', __name__)

@planos_routes.route("/planos", methods=["GET"])
def listar_planos():
    planos = Plano.query.all()
    return jsonify([p.to_dict() for p in planos]), 200

@planos_routes.route("/planos", methods=["POST"])
def criar_plano():
    data = request.get_json()
    plano = Plano(
        nome=data["nome"],
        descricao=data.get("descricao", ""),
        preco=data.get("preco", 0.0),
        duracao_dias=data["duracao_dias"]
    )
    db.session.add(plano)
    db.session.commit()
    return jsonify(plano.to_dict()), 201