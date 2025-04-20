from models import db

class Especie(db.Model):
    __tablename__ = 'especies'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    racas = db.relationship("Raca", backref="especie", lazy=True)