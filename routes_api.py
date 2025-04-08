# routes.py
from flask import Blueprint, jsonify, request
from auth import login, cadastro
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Animal, Usuario, Match, Like, Mensagem, Notificacao
from flask_socketio import SocketIO, emit, join_room, leave_room
import math

socketio = SocketIO()

routes = Blueprint('routes', __name__)

@routes.route('/login', methods=['POST'])
def login_route():
    return login()

@routes.route('/cadastro', methods=['POST'])
def cadastro_route():
    return cadastro()

def criar_notificacao(usuario_id, mensagem):
    nova_notificacao = Notificacao(usuario_id=usuario_id, mensagem=mensagem)
    db.session.add(nova_notificacao)
    db.session.commit()

def notificacao_match(animal1, animal2):
    criar_notificacao(animal1.usuario_id, f"Seu pet {animal1.nome} deu match com {animal2.nome}!")
    criar_notificacao(animal2.usuario_id, f"Seu pet {animal2.nome} deu match com {animal1.nome}!")


@routes.route("/animais", methods=["GET"])
@jwt_required()  # Protege a rota com o JWT
def animais():
    current_user = get_jwt_identity()  # Obtém o ID do usuário logado
    animais = Animal.query.all()
    return jsonify([animal.to_json() for animal in animais])

@routes.route("/animais", methods=["POST"])
@jwt_required()  # Protegendo a rota
def adicionar_animal():
    try:
        current_user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado
        data = request.get_json()

        if not data or not data.get("nome") or not data.get("especie") or not data.get("raca") or not data.get("idade") or not data.get("especie"):
            return jsonify({"message": "Nome e espécie são obrigatórios!"}), 400

        novo_animal = Animal(
            nome=data["nome"],
            especie=data["especie"],
            raca=data["raca"],
            idade=data.get("idade"),
            descricao=data.get("descricao"),
            imagem_url=data.get("imagem_url"),
            localizacao=data.get("localizacao"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            usuario_id=current_user_id  # Associa o animal ao usuário logado

        )
        
        db.session.add(novo_animal)
        db.session.commit()

        return jsonify(novo_animal.to_json()), 201
    
    except Exception as e:
        print(f"Erro ao adicionar animal: {e}")
        return jsonify({"message": "Erro interno no servidor"}), 500

    
@routes.route("/meus-animais", methods=["GET"])
@jwt_required()
def listar_meus_animais():
    current_user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado
    meus_animais = Animal.query.filter_by(usuario_id=current_user_id).all()
    
    return jsonify([animal.to_json() for animal in meus_animais]), 200


@routes.route("/meus-animais/<int:animal_id>", methods=["PUT"])
@jwt_required()
def editar_animal(animal_id):
    current_user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado
    animal = Animal.query.filter_by(id=animal_id, usuario_id=current_user_id).first()

    if not animal:
        return jsonify({"message": "Animal não encontrado ou não pertence ao usuário!"}), 404

    data = request.get_json()
    
    animal.nome = data.get("nome", animal.nome)
    animal.especie = data.get("especie", animal.especie)
    animal.idade = data.get("idade", animal.idade)
    animal.descricao = data.get("descricao", animal.descricao)
    animal.imagem_url = data.get("imagem_url", animal.imagem_url)
    animal.localizacao = data.get("localizacao", animal.localizacao)

    db.session.commit()
    return jsonify(animal.to_json()), 200



@routes.route("/meus-animais/<int:animal_id>", methods=["DELETE"])
@jwt_required()
def deletar_animal(animal_id):
    current_user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado
    animal = Animal.query.filter_by(id=animal_id, usuario_id=current_user_id).first()

    if not animal:
        return jsonify({"message": "Animal não encontrado ou não pertence ao usuário!"}), 404

    db.session.delete(animal)
    db.session.commit()
    return jsonify({"message": "Animal deletado com sucesso!"}), 200



@routes.route('/like', methods=['POST'])
def like_animal():
    data = request.json
    liker_id = data.get('liker_id')
    liked_id = data.get('liked_id')
    
    # Verifica se já existe um like recíproco
    existing_match = Match.query.filter_by(animal1_id=liked_id, animal2_id=liker_id).first()
    if existing_match:
        return jsonify({"message": "Match encontrado!", "match": existing_match.to_dict()}), 201
    
    # Se não houver match ainda, salva o like
    new_match = Match(animal1_id=liker_id, animal2_id=liked_id)
    db.session.add(new_match)
    db.session.commit()
    return jsonify({"message": "Like registrado! Aguarde um match."}), 201


@routes.route('/match', methods=['POST'])
@jwt_required()
def match():
    current_user = get_jwt_identity()

    data = request.get_json()
    animal_id = data.get('animal_id')
    liked_animal_id = data.get('liked_animal_id')

    # Verificar se os IDs são válidos
    animal = Animal.query.get(animal_id)
    liked_animal = Animal.query.get(liked_animal_id)

    if not animal or not liked_animal:
        return jsonify({"message": "Animal não encontrado!"}), 404

    # Verificar se o usuário é o dono do animal
    if animal.usuario_id != current_user:
        return jsonify({"message": "Você não tem permissão para curtir esse animal!"}), 403

    # Criar o like
    like = Like(usuario_id=current_user, animal_id=animal_id, liked_animal_id=liked_animal_id)
    db.session.add(like)
    db.session.commit()

    # Verificar se o animal curtiu de volta
    reverse_like = Like.query.filter_by(usuario_id=liked_animal.usuario_id, animal_id=liked_animal_id, liked_animal_id=animal_id).first()
    if reverse_like:
        return jsonify({"message": "Match realizado!", "match": True}), 200
    else:
        return jsonify({"message": "Curtido com sucesso!", "match": False}), 200


@routes.route('/like', methods=['POST'])
@jwt_required()
def like():
    current_user = get_jwt_identity()

    data = request.get_json()
    animal_id = data.get('animal_id')
    liked_animal_id = data.get('liked_animal_id')

    # Verificar se os IDs são válidos
    animal = Animal.query.get(animal_id)
    liked_animal = Animal.query.get(liked_animal_id)

    if not animal or not liked_animal:
        return jsonify({"message": "Animal não encontrado!"}), 404

    # Verificar se o usuário é o dono do animal
    if animal.usuario_id != current_user:
        return jsonify({"message": "Você não tem permissão para curtir esse animal!"}), 403

    # Criar o like
    like = Like(usuario_id=current_user, animal_id=animal_id, liked_animal_id=liked_animal_id)
    db.session.add(like)
    db.session.commit()

    return jsonify({"message": "Curtido com sucesso!"}), 200


@routes.route('/matches', methods=['GET'])
@jwt_required()
def view_matches():
    current_user = get_jwt_identity()

    # Encontrar todos os likes realizados pelo usuário
    likes = Like.query.filter_by(usuario_id=current_user).all()

    matches = []
    for like in likes:
        reverse_like = Like.query.filter_by(usuario_id=like.liked_animal_id, animal_id=like.liked_animal_id, liked_animal_id=like.animal_id).first()
        if reverse_like:
            matches.append({
                "animal_1": Animal.query.get(like.animal_id).to_json(),
                "animal_2": Animal.query.get(like.liked_animal_id).to_json()
            })

    return jsonify(matches)

def enviar_notificacao(destinatario_id, mensagem):
    """Envia uma notificação em tempo real para o destinatário via WebSocket."""
    socketio.emit(f'notificacao_{destinatario_id}', {'mensagem': mensagem}, room=destinatario_id)


@socketio.on('connect')
def handle_connect():
    user_id = request.args.get('user_id')
    if user_id:
        join_room(user_id)
        print(f'Usuário {user_id} conectado.')

@socketio.on('disconnect')
def handle_disconnect():
    user_id = request.args.get('user_id')
    if user_id:
        leave_room(user_id)
        print(f'Usuário {user_id} desconectado.')


@socketio.on('join')
def join(data):
    user_id = data.get('user_id')
    if user_id:
        join_room(user_id)
        print(f'Usuário {user_id} entrou na sala.')

@socketio.on('leave')
def leave(data):
    user_id = data.get('user_id')
    if user_id:
        leave_room(user_id)
        print(f'Usuário {user_id} saiu da sala.')

@routes.route('/enviar_mensagem', methods=['POST'])
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

    # Envia notificação para o destinatário
    enviar_notificacao(destinatario_id, conteudo)

    return {"mensagem": "Mensagem enviada com sucesso!"}, 201


@routes.route('/chat/<int:destinatario_id>', methods=['GET'])
@jwt_required()
def ver_mensagens(destinatario_id):
    current_user = get_jwt_identity()

    # Verificar se o destinatário existe
    destinatario = Usuario.query.get(destinatario_id)
    if not destinatario:
        return jsonify({"message": "Destinatário não encontrado!"}), 404

    # Verificar se há match entre os donos
    match = Like.query.filter(
        (Like.usuario_id == current_user and Like.liked_animal_id == destinatario_id) |
        (Like.usuario_id == destinatario_id and Like.liked_animal_id == current_user)
    ).first()

    if not match:
        return jsonify({"message": "Você precisa primeiro dar match para ver as mensagens!"}), 403

    # Paginação
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


@routes.route('/chat/mark_as_read', methods=['POST'])
@jwt_required()
def marcar_como_lido():
    current_user = get_jwt_identity()

    data = request.get_json()
    mensagem_id = data.get('mensagem_id')

    mensagem = Mensagem.query.get(mensagem_id)
    if not mensagem:
        return jsonify({"message": "Mensagem não encontrada!"}), 404

    # Verificar se a mensagem é destinada ao usuário atual
    if mensagem.destinatario_id != current_user:
        return jsonify({"message": "Você não pode marcar esta mensagem como lida!"}), 403

    # Marcar a mensagem como lida
    mensagem.lido = True
    db.session.commit()

    return jsonify({"message": "Mensagem marcada como lida!"}), 200



@routes.route('/notificacoes', methods=['GET'])
@jwt_required()
def obter_notificacoes():
    usuario_id = get_jwt_identity()
    notificacoes = Notificacao.query.filter_by(usuario_id=usuario_id).all()
    return jsonify([{'id': n.id, 'mensagem': n.mensagem, 'lida': n.lida, 'data_criacao': n.data_criacao} for n in notificacoes])

@routes.route('/notificacoes/<int:notificacao_id>', methods=['PATCH'])
@jwt_required()
def marcar_notificacao_como_lida(notificacao_id):
    usuario_id = get_jwt_identity()
    notificacao = Notificacao.query.filter_by(id=notificacao_id, usuario_id=usuario_id).first()
    if not notificacao:
        return jsonify({'erro': 'Notificação não encontrada'}), 404
    notificacao.lida = True
    db.session.commit()
    return jsonify({'mensagem': 'Notificação marcada como lida'})


def calcular_distancia(lat1, lon1, lat2, lon2):
    # Converte as coordenadas de graus para radianos
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Fórmula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Raio da Terra em quilômetros
    R = 6371
    distancia = R * c
    return distancia


@routes.route("/animais", methods=["GET"])
@jwt_required()
def listar_animais():
    current_user_id = get_jwt_identity()  # Obtém o ID do usuário autenticado

    # Parâmetros de filtro
    nome = request.args.get('nome')
    especie = request.args.get('especie')
    lat = float(request.args.get('lat'))  # Latitude do ponto de busca
    lon = float(request.args.get('lon'))  # Longitude do ponto de busca
    raio = float(request.args.get('raio', 10))  # Raio de busca (em km), default 10 km

    # Inicia a consulta básica
    query = Animal.query.filter_by(usuario_id=current_user_id)

    # Aplica filtros com base nos parâmetros fornecidos
    if nome:
        query = query.filter(Animal.nome.ilike(f"%{nome}%"))
    if especie:
        query = query.filter(Animal.especie.ilike(f"%{especie}%"))

    # Filtra animais baseados na proximidade usando a fórmula de Haversine
    animais_proximos = []
    for animal in query.all():
        distancia = calcular_distancia(lat, lon, animal.latitude, animal.longitude)
        if distancia <= raio:  # Apenas animais dentro do raio especificado
            animais_proximos.append(animal)

    # Retorna os animais próximos
    return jsonify([animal.to_json() for animal in animais_proximos]), 200
