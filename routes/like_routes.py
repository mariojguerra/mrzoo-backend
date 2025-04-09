from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Like, Match, Animal

like_routes = Blueprint('like_routes', __name__)

@like_routes.route('/like', methods=['POST'])
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

    # Verifica se o like é recíproco
    reverse_like = Like.query.filter_by(
        usuario_id=liked_animal.usuario_id,
        animal_id=liked_animal_id,
        liked_animal_id=animal_id
    ).first()

    if reverse_like:
        # Cria o match se for mútuo
        match = Match(animal1_id=animal_id, animal2_id=liked_animal_id)
        db.session.add(match)
        db.session.commit()
        return jsonify({"message": "Match realizado!", "match": True}), 200

    return jsonify({"message": "Curtido com sucesso!", "match": False}), 200


@like_routes.route('/matches', methods=['GET'])
@jwt_required()
def view_matches():
    current_user = get_jwt_identity()
    likes = Like.query.filter_by(usuario_id=current_user).all()

    matches = []
    for like in likes:
        reverse_like = Like.query.filter_by(
            usuario_id=like.liked_animal_id,
            animal_id=like.liked_animal_id,
            liked_animal_id=like.animal_id
        ).first()
        if reverse_like:
            matches.append({
                "animal_1": Animal.query.get(like.animal_id).to_json(),
                "animal_2": Animal.query.get(like.liked_animal_id).to_json()
            })

    return jsonify(matches), 200
