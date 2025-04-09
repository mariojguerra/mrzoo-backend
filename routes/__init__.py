# __init__.py

from flask import Blueprint
from flask_socketio import SocketIO

from .auth_routes import auth_routes
from .especie_routes import especie_routes
from .raca_routes import raca_routes
from .animal_routes import animal_routes
from .uploads import upload_routes
from .match_routes import match_routes
from .chat_routes import chat_routes
from .notificacao_routes import notificacao_routes
from .like_routes import like_routes
from .explorar_routes import explorar_routes

routes = Blueprint('routes', __name__)
socketio = SocketIO()

# Registro dos blueprints

routes.register_blueprint(auth_routes)
routes.register_blueprint(especie_routes)
routes.register_blueprint(raca_routes)
routes.register_blueprint(animal_routes)
routes.register_blueprint(upload_routes, url_prefix="/uploads")
routes.register_blueprint(match_routes)
routes.register_blueprint(chat_routes)
routes.register_blueprint(notificacao_routes)
routes.register_blueprint(like_routes)
routes.register_blueprint(explorar_routes)

