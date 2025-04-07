from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
import datetime

# Inicializa o Flask
app = Flask(__name__)
app.debug = True  # Habilita o modo de depuração para ver os detalhes dos erros

# Configuração do banco de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mrzoo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Chave secreta
SECRET_KEY = '2404@Theo'

# Gerando o token
payload = {
    'sub': 'user123',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira em 1 hora
}

token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
print(token)  # Verifique o token gerado

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = SECRET_KEY
jwt = JWTManager(app)

# Inicializa o banco de dados e criptografia
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Modelo de dados
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer)
    descricao = db.Column(db.Text)
    imagem_url = db.Column(db.String(255))
    localizacao = db.Column(db.String(100))

    def to_json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "especie": self.especie,
            "idade": self.idade,
            "descricao": self.descricao,
            "imagem_url": self.imagem_url,
            "localizacao": self.localizacao
        }

# Modelo de usuário
# Modelo do usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username
        }
    
@app.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        data = request.get_json()

        # Verificar se o corpo da requisição contém os campos obrigatórios
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'message': 'Nome de usuário e senha são obrigatórios!'}), 400

        username = data.get('username')
        password = data.get('password')

        # Verificar se o nome de usuário já existe
        user_exists = Usuario.query.filter_by(username=username).first()
        if user_exists:
            return jsonify({'message': 'Usuário já existe!'}), 400

        # Criação do novo usuário
        novo_usuario = Usuario(username=username)
        novo_usuario.set_password(password)
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({'message': 'Usuário criado com sucesso!'}), 201
    except Exception as e:
        # Logar o erro detalhado para facilitar o diagnóstico
        print(f"Erro no cadastro: {e}")
        return jsonify({'message': 'Erro interno no servidor!'}), 500



@app.route('/protegido', methods=['GET'])
@jwt_required()
def protegido():
    token = request.headers.get('Authorization')  # Expectativa: "Bearer <token>"
    if not token:
        return jsonify({'message': 'Token de autenticação ausente!'}), 401

    try:
        token = token.split(" ")[1]  # Pega apenas o token (sem o "Bearer")
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        user_id = decoded_token['sub']
        usuario = Usuario.query.get(user_id)

        if usuario:
            return jsonify({'message': 'Acesso autorizado', 'user': usuario.to_json()}), 200
        else:
            return jsonify({'message': 'Usuário não encontrado!'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expirado!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Token inválido!'}), 401


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Nome de usuário e senha são obrigatórios!'}), 400

    usuario = Usuario.query.filter_by(username=username).first()
    if usuario and usuario.check_password(password):
        # Gerar o token JWT
        access_token = create_access_token(identity=str(usuario.id))  # Convertendo ID para string

        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Credenciais inválidas!'}), 401


# Rota protegida (exemplo)
@app.route("/animais", methods=["GET"])
@jwt_required()  # Protege a rota com o JWT
def animais():
    current_user = get_jwt_identity()  # Obtém o ID do usuário logado
    animais = Animal.query.all()
    return jsonify([animal.to_json() for animal in animais])

@app.route("/animais", methods=["POST"])
@jwt_required()  # Protegendo a rota
def adicionar_animal():
    try:
        data = request.get_json()

        if not data or not data.get("nome") or not data.get("especie"):
            return jsonify({"message": "Nome e espécie são obrigatórios!"}), 400

        novo_animal = Animal(
            nome=data["nome"],
            especie=data["especie"],
            idade=data.get("idade"),
            descricao=data.get("descricao"),
            imagem_url=data.get("imagem_url"),
            localizacao=data.get("localizacao")
        )
        
        db.session.add(novo_animal)
        db.session.commit()

        return jsonify(novo_animal.to_json()), 201

    except Exception as e:
        print(f"Erro ao adicionar animal: {e}")
        return jsonify({"message": "Erro interno no servidor"}), 500

# Executa a aplicação
if __name__ == "__main__":
    app.run(debug=True)