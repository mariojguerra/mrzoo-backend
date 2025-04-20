from models import db


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