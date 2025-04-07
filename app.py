# app.py
from flask import Flask
from config import Config
from models import db
from routes_api import routes, socketio

from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_socketio import SocketIO, emit

import os
import geventwebsocket


app = Flask(__name__)
app.debug = True

socketio.init_app(app)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'mrzoo.db')}"

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configuração para upload de imagens
app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'  # Pasta onde as imagens serão salvas
app.config['UPLOADED_IMAGES_ALLOW'] = IMAGES  # Tipo de arquivo permitido

# Configurando o Flask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

# Chave secreta
SECRET_KEY = '2404@Theo'

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

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

