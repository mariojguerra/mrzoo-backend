from flask import Blueprint, jsonify
from utils.assinatura_utils import verifica_assinatura_ativa

premium_routes = Blueprint("premium_routes", __name__, url_prefix="/premium")

@premium_routes.route("/recurso", methods=["GET"])
@verifica_assinatura_ativa()
def recurso_premium():
    return jsonify({"msg": "Você tem acesso ao recurso Premium!"})
