from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Animal, db
from sqlalchemy import or_

explorar_routes = Blueprint('explorar_routes', __name__)


def calcular_distancia(lat1, lon1, lat2, lon2):
    import math
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371
    return R * c


@explorar_routes.route("/explorar", methods=["GET"])
@jwt_required()
def explorar_animais():
    current_user = get_jwt_identity()
    especie_id = request.args.get("especie_id", type=int)
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    raio = request.args.get("raio", 50, type=float)

    if not especie_id or lat is None or lon is None:
        return jsonify({"erro": "Parâmetros obrigatórios: especie_id, lat, lon"}), 400

    animais = Animal.query.filter(Animal.usuario_id != current_user, Animal.especie_id == especie_id).all()
    animais_proximos = []

    for animal in animais:
        if animal.latitude and animal.longitude:
            distancia = calcular_distancia(lat, lon, animal.latitude, animal.longitude)
            if distancia <= raio:
                animais_proximos.append(animal)

    return jsonify([animal.to_json() for animal in animais_proximos]), 200