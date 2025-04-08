# app.py
from flask import Flask
from config import Config
from models import db
from routes_api import routes, socketio

from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit

import os
import gunicorn

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

app = Flask(__name__)
app.debug = True

socketio.init_app(app, async_mode='gevent')

#BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'mrzoo.db')}"

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = SECRET_KEY

# Inicializa o banco de dados
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Inicializa o JWT
jwt = JWTManager(app)

@socketio.on('connect')
def handle_connect():
    print("Usuário conectado!")
    emit('status', {'message': 'Você está conectado!'})

@socketio.on('message')
def handle_message(msg):
    print(f"Mensagem recebida: {msg}")
    emit('new_message', msg, broadcast=True)  # Envia a mensagem para todos os usuários conectados


# Registra as rotas
app.register_blueprint(routes)


@app.route("/")
def home():
    return "API do MrZoo está rodando!"

application = app  # <- necessário para o Gunicorn encontrar sua app

if __name__ == "__main__":
    import gevent
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

