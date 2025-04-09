from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Especie

especie_routes = Blueprint('especie_routes', __name__)

@especie_routes.route('/especies', methods=['POST'])
@jwt_required()
def criar_especie():
    data = request.get_json()
    nome = data.get('nome')

    if not nome:
        return jsonify({"erro": "Nome é obrigatório."}), 400

    especie = Especie(nome=nome)
    db.session.add(especie)
    db.session.commit()

    return jsonify({"id": especie.id, "nome": especie.nome}), 201

@especie_routes.route('/especies/lote', methods=['POST'])
@jwt_required()
def adicionar_especies():
    try:
        dados = request.get_json()

        if not isinstance(dados, list):
            return jsonify({"erro": "Esperado uma lista de espécies"}), 400

        novas_especies = []
        for item in dados:
            nome = item.get("nome")
            if not nome:
                continue  # pula se não tiver nome
            especie = Especie(nome=nome)
            novas_especies.append(especie)

        if not novas_especies:
            return jsonify({"erro": "Nenhuma espécie válida fornecida"}), 400

        db.session.add_all(novas_especies)
        db.session.commit()

        return jsonify({"mensagem": f"{len(novas_especies)} espécies adicionadas com sucesso"}), 201

    except Exception as e:
        print(f"Erro ao adicionar espécies: {e}")
        return jsonify({"erro": "Erro interno no servidor"}), 500
