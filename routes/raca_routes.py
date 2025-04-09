from flask import Blueprint, request, jsonify
from models import db, Raca
from flask_jwt_extended import jwt_required

raca_routes = Blueprint('raca_routes', __name__)

@raca_routes.route('/racas', methods=['POST'])
@jwt_required()
def criar_racas():
    dados = request.get_json()

    if not isinstance(dados, list):
        return jsonify({"erro": "Esperado uma lista de raças"}), 400

    novas_racas = []
    for item in dados:
        nome = item.get("nome")
        especie_id = item.get("especie_id")

        if not nome or not especie_id:
            continue

        nova_raca = Raca(nome=nome, especie_id=especie_id)
        novas_racas.append(nova_raca)

    if not novas_racas:
        return jsonify({"erro": "Nenhuma raça válida fornecida"}), 400

    db.session.add_all(novas_racas)
    db.session.commit()

    return jsonify({"mensagem": f"{len(novas_racas)} raças adicionadas com sucesso"}), 201


@raca_routes.route('/racas', methods=['GET'])
def listar_racas():
    especie_id = request.args.get('especie_id')

    if especie_id:
        racas = Raca.query.filter_by(especie_id=especie_id).all()
    else:
        racas = Raca.query.all()

    return jsonify([{"id": r.id, "nome": r.nome, "especie_id": r.especie_id} for r in racas])


@raca_routes.route('/racas/<int:raca_id>', methods=['GET'])
def obter_raca(raca_id):
    raca = Raca.query.get(raca_id)
    if not raca:
        return jsonify({"erro": "Raça não encontrada"}), 404

    return jsonify({"id": raca.id, "nome": raca.nome, "especie_id": raca.especie_id})


@raca_routes.route('/racas/<int:raca_id>', methods=['PUT'])
@jwt_required()
def atualizar_raca(raca_id):
    raca = Raca.query.get(raca_id)
    if not raca:
        return jsonify({"erro": "Raça não encontrada"}), 404

    dados = request.get_json()
    raca.nome = dados.get("nome", raca.nome)
    raca.especie_id = dados.get("especie_id", raca.especie_id)

    db.session.commit()
    return jsonify({"mensagem": "Raça atualizada com sucesso"})


@raca_routes.route('/racas/<int:raca_id>', methods=['DELETE'])
@jwt_required()
def deletar_raca(raca_id):
    raca = Raca.query.get(raca_id)
    if not raca:
        return jsonify({"erro": "Raça não encontrada"}), 404

    db.session.delete(raca)
    db.session.commit()
    return jsonify({"mensagem": "Raça deletada com sucesso"})
