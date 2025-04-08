# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import Float
import json

db = SQLAlchemy()
bcrypt = Bcrypt()

class Especie(db.Model):
    __tablename__ = 'especies'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    racas = db.relationship("Raca", backref="especie", lazy=True)

class Raca(db.Model):
    __tablename__ = 'racas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especie_id = db.Column(db.Integer, db.ForeignKey('especies.id'), nullable=False)
    animais = db.relationship('Animal', backref='raca_obj', lazy=True)



class ImagemAnimal(db.Model):
    __tablename__ = 'imagens_animais'

    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.String, db.ForeignKey('animal.id'), nullable=False)
    url = db.Column(db.String, nullable=False)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)

    def to_json(self):
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "url": self.url,
            "data_upload": self.data_upload.isoformat()
        }

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_animal = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer)
    descricao = db.Column(db.Text)
    imagem_url = db.Column(db.String(255))
    localizacao = db.Column(db.String(100))
    latitude = db.Column(Float)  # Adicionando Latitude
    longitude = db.Column(Float)  # Adicionando Longitude
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Chave estrangeira
    especie_id = db.Column(db.Integer, db.ForeignKey('especies.id'), nullable=False)
    raca_id = db.Column(db.Integer, db.ForeignKey('racas.id'), nullable=False)    
    imagens = db.relationship("ImagemAnimal", backref="animal", lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "id_animal": self.id_animal,
            "nome": self.nome,
            "especie": self.especie,
            "raca": self.raca,
            "idade": self.idade,
            "descricao": self.descricao,
            "imagem_url": self.imagem_url,
            "localizacao": self.localizacao,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "imagens": [img.to_json() for img in self.imagens]
        }

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    animais = db.relationship('Animal', backref='usuario', lazy=True)
    likes = db.relationship('Like', backref='usuario', lazy=True)
    notificacoes = db.relationship('Notificacao', backref='usuario', lazy=True)


    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'animais': [animal.to_json() for animal in self.animais]  # Lista de animais do usuário

        }


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal1_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    animal2_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "animal1_id": self.animal1_id,
            "animal2_id": self.animal2_id,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    liked_animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "animal_id": self.animal_id,
            "liked_animal_id": self.liked_animal_id
        }
    

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remetente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    destinatario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    lido = db.Column(db.Boolean, default=False)  # Campo para marcar como lido

    # Relacionamentos
    remetente = db.relationship('Usuario', foreign_keys=[remetente_id])
    destinatario = db.relationship('Usuario', foreign_keys=[destinatario_id])

    def to_json(self):
        return {
            "id": self.id,
            "remetente_id": self.remetente_id,
            "destinatario_id": self.destinatario_id,
            "conteudo": self.conteudo,
            "data_envio": self.data_envio.isoformat(),
            "lido": self.lido,
            "remetente_username": self.remetente.username,
            "destinatario_username": self.destinatario.username
        }


class Notificacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    mensagem = db.Column(db.String(255), nullable=False)
    lida = db.Column(db.Boolean, default=False)
    criada_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'mensagem': self.mensagem,
            'lida': self.lida,
            'criada_em': self.criada_em.strftime('%Y-%m-%d %H:%M:%S')
        }

