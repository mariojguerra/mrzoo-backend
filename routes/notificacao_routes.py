from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Notificacao

notificacao_routes = Blueprint("notificacao_routes", __name__)

def criar_notificacao(usuario_id, mensagem):
    nova_notificacao = Notificacao(usuario_id=usuario_id, mensagem=mensagem)
    db.session.add(nova_notificacao)
    db.session.commit()

def notificacao_match(animal1, animal2):
    criar_notificacao(animal1.usuario_id, f"Seu pet {animal1.nome} deu match com {animal2.nome}!")
    criar_notificacao(animal2.usuario_id, f"Seu pet {animal2.nome} deu match com {animal1.nome}!")


@notificacao_routes.route('/notificacoes', methods=['GET'])
@jwt_required()
def obter_notificacoes():
    usuario_id = get_jwt_identity()
    notificacoes = Notificacao.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([
        {
            'id': n.id,
            'mensagem': n.mensagem,
            'lida': n.lida,
            'criada_em': n.criada_em.strftime('%Y-%m-%d %H:%M:%S')
        } for n in notificacoes
    ])


@notificacao_routes.route('/notificacoes/<int:notificacao_id>', methods=['PATCH'])
@jwt_required()
def marcar_notificacao_como_lida(notificacao_id):
    usuario_id = get_jwt_identity()
    notificacao = Notificacao.query.filter_by(id=notificacao_id, usuario_id=usuario_id).first()

    if not notificacao:
        return jsonify({'erro': 'Notificacao não encontrada'}), 404

    notificacao.lida = True
    db.session.commit()
    return jsonify({'mensagem': 'Notificação marcada como lida'})
