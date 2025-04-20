from sqlalchemy.dialects.mysql import DOUBLE
from models import db


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
