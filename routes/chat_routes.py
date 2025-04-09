from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Usuario, Mensagem, Like
from flask_socketio import emit, join_room, leave_room
from datetime import datetime

chat_routes = Blueprint("chat_routes", __name__)

@chat_routes.route('/enviar_mensagem', methods=['POST'])
@jwt_required()
def enviar_mensagem():
    remetente_id = get_jwt_identity()
    dados = request.json
    destinatario_id = dados.get('destinatario_id')
    conteudo = dados.get('conteudo')

    if not destinatario_id or not conteudo:
        return {"erro": "Dados inválidos"}, 400

    nova_msg = Mensagem(remetente_id=remetente_id, destinatario_id=destinatario_id, conteudo=conteudo)
    db.session.add(nova_msg)
    db.session.commit()

    emit(f'notificacao_{destinatario_id}', {'mensagem': conteudo}, room=destinatario_id)

    return {"mensagem": "Mensagem enviada com sucesso!"}, 201


@chat_routes.route('/chat/<int:destinatario_id>', methods=['GET'])
@jwt_required()
def ver_mensagens(destinatario_id):
    current_user = get_jwt_identity()

    destinatario = Usuario.query.get(destinatario_id)
    if not destinatario:
        return jsonify({"message": "Destinatário não encontrado!"}), 404

    match = Like.query.filter(
        (Like.usuario_id == current_user and Like.liked_animal_id == destinatario_id) |
        (Like.usuario_id == destinatario_id and Like.liked_animal_id == current_user)
    ).first()

    if not match:
        return jsonify({"message": "Você precisa primeiro dar match para ver as mensagens!"}), 403

    page = request.args.get('page', 1, type=int)
    per_page = 10
    mensagens = Mensagem.query.filter(
        (Mensagem.remetente_id == current_user and Mensagem.destinatario_id == destinatario_id) |
        (Mensagem.remetente_id == destinatario_id and Mensagem.destinatario_id == current_user)
    ).order_by(Mensagem.data_envio.asc()).paginate(page, per_page, False)

    return jsonify({
        "mensagens": [mensagem.to_json() for mensagem in mensagens.items],
        "next_page": mensagens.next_num,
        "prev_page": mensagens.prev_num
    })


@chat_routes.route('/chat/mark_as_read', methods=['POST'])
@jwt_required()
def marcar_como_lido():
    current_user = get_jwt_identity()

    data = request.get_json()
    mensagem_id = data.get('mensagem_id')

    mensagem = Mensagem.query.get(mensagem_id)
    if not mensagem:
        return jsonify({"message": "Mensagem não encontrada!"}), 404

    if mensagem.destinatario_id != current_user:
        return jsonify({"message": "Você não pode marcar esta mensagem como lida!"}), 403

    mensagem.lido = True
    db.session.commit()

    return jsonify({"message": "Mensagem marcada como lida!"}), 200
