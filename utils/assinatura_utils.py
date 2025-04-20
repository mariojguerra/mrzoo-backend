from functools import wraps
from flask import jsonify, request
from datetime import datetime
from models import Assinatura, db
from models import Usuario  # ou sua lógica de autenticação
from flask_jwt_extended import get_jwt_identity


def get_usuario_logado():
    usuario_id = get_jwt_identity()
    return Usuario.query.get(usuario_id)

def verifica_assinatura_ativa():
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            usuario = get_usuario_logado()
            assinatura = (
                Assinatura.query
                .filter_by(usuario_id=usuario.id, ativa=True)
                .order_by(Assinatura.inicio.desc())
                .first()
            )
            if not assinatura:
                return jsonify({"error": "Assinatura não encontrada"}), 403

            if assinatura.fim and assinatura.fim < datetime.utcnow():
                assinatura.ativa = False
                db.session.commit()
                return jsonify({"error": "Assinatura expirada"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator

def verifica_modulo_permitido(modulo_necessario: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            usuario = get_usuario_logado()
            assinatura = (
                Assinatura.query
                .filter_by(usuario_id=usuario.id, ativa=True)
                .order_by(Assinatura.inicio.desc())
                .first()
            )
            if not assinatura or not assinatura.plano:
                return jsonify({"error": "Sem assinatura ativa"}), 403

            if assinatura.fim and assinatura.fim < datetime.utcnow():
                assinatura.ativa = False
                db.session.commit()
                return jsonify({"error": "Assinatura expirada"}), 403

            nomes_modulos = [m.modulo.nome for m in assinatura.plano.modulos]
            if modulo_necessario not in nomes_modulos:
                return jsonify({"error": f"Acesso negado ao módulo: {modulo_necessario}"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator

