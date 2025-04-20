from models import db

class Modulo(db.Model):
    __tablename__ = "modulos"
    __table_args__ = {'mysql_charset': 'utf8mb4'}


    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)  # Ex: "Chat", "Swipe", "Ranking", etc.

    def to_dict(self):
        return {"id": self.id, "nome": self.nome}