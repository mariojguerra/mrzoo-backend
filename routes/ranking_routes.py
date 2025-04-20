from flask import Blueprint, jsonify
from utils.assinatura_utils import verifica_modulo_permitido

ranking_routes = Blueprint("ranking_routes", __name__, url_prefix="/ranking")

@ranking_routes.route("/", methods=["GET"])
@verifica_modulo_permitido("Ranking")
def acessar_ranking():
    return jsonify({"msg": "Ranking Premium acessado com sucesso!"})
