from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Plano, Assinatura
from datetime import datetime, timedelta

assinatura_routes = Blueprint('assinatura_routes', __name__)

@assinatura_routes.route("/assinaturas", methods=["POST"])
@jwt_required()
def criar_assinatura():
    data = request.get_json()
    usuario = get_jwt_identity()
    plano = Plano.query.get(data["plano_id"])
    if not plano:
        return jsonify({"error": "Plano não encontrado"}), 404

    inicio = datetime.utcnow()
    fim = inicio + timedelta(days=plano.duracao_dias)

    assinatura = Assinatura(
        usuario_id=usuario.id,
        plano_id=plano.id,
        inicio=inicio,
        fim=fim,
        ativa=True
    )
    db.session.add(assinatura)
    db.session.commit()
    return jsonify(assinatura.to_dict()), 201

@assinatura_routes.route("/assinaturas/me", methods=["GET"])
@jwt_required()
def minha_assinatura():
    usuario = get_jwt_identity()
    assinatura = Assinatura.query.filter_by(usuario_id=usuario.id, ativa=True).order_by(Assinatura.inicio.desc()).first()
    if not assinatura:
        return jsonify({"error": "Nenhuma assinatura ativa"}), 404
    return jsonify(assinatura.to_dict()), 200