# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import Float
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()
bcrypt = Bcrypt()

class Especie(db.Model):
    __tablename__ = 'especies'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    racas = db.relationship("Raca", backref="especie", lazy=True)

class Raca(db.Model):
    __tablename__ = 'racas'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    especie_id = db.Column(db.Integer, db.ForeignKey('especies.id'), nullable=False)
    animais = db.relationship('Animal', backref='raca_obj', lazy=True)

class ImagemAnimal(db.Model):
    __tablename__ = 'imagens_animais'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)

    def to_json(self):
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "url": self.url,
            "data_upload": self.data_upload.isoformat()
        }

class Animal(db.Model):
    __tablename__ = 'animal'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_animal = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(50), nullable=False)
    raca = db.Column(db.String(50), nullable=False)
    idade = db.Column(db.Integer)
    descricao = db.Column(db.Text)
    imagem_url = db.Column(db.String(255))
    localizacao = db.Column(db.String(100))
    latitude = db.Column(DOUBLE)
    longitude = db.Column(DOUBLE)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
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
    __tablename__ = 'usuario'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
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
            'animais': [animal.to_json() for animal in self.animais]
        }

class Match(db.Model):
    __tablename__ = 'match'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    __tablename__ = 'like'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    __tablename__ = 'mensagem'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    remetente_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    destinatario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    lido = db.Column(db.Boolean, default=False)

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
    __tablename__ = 'notificacao'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

class Plano(db.Model):
    __tablename__ = "planos"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Float, default=0.0)
    duracao_dias = db.Column(db.Integer, nullable=False)

    modulos = db.relationship("PlanoModulo", back_populates="plano")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "duracao_dias": self.duracao_dias,
            "modulos": [m.modulo.nome for m in self.modulos]
        }
    
class Assinatura(db.Model):
    __tablename__ = "assinaturas"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey("planos.id"), nullable=False)
    inicio = db.Column(db.DateTime, default=datetime.utcnow)
    fim = db.Column(db.DateTime)
    ativa = db.Column(db.Boolean, default=True)

    plano = db.relationship("Plano", backref="assinaturas")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "plano": self.plano.to_dict() if self.plano else None,
            "inicio": self.inicio.isoformat(),
            "fim": self.fim.isoformat() if self.fim else None,
            "ativa": self.ativa
        }
    
class Modulo(db.Model):
    __tablename__ = "modulos"
    __table_args__ = {'mysql_charset': 'utf8mb4'}


    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)  # Ex: "Chat", "Swipe", "Ranking", etc.

    def to_dict(self):
        return {"id": self.id, "nome": self.nome}
    
class PlanoModulo(db.Model):
    __tablename__ = "plano_modulos"
    __table_args__ = {'mysql_charset': 'utf8mb4'}


    id = db.Column(db.Integer, primary_key=True)
    plano_id = db.Column(db.Integer, db.ForeignKey("planos.id"))
    modulo_id = db.Column(db.Integer, db.ForeignKey("modulos.id"))

    plano = db.relationship("Plano", back_populates="modulos")
    modulo = db.relationship("Modulo", back_populates="planos")
