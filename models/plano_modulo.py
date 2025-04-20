
from models import db

class PlanoModulo(db.Model):
    __tablename__ = "plano_modulos"
    __table_args__ = {'mysql_charset': 'utf8mb4'}


    id = db.Column(db.Integer, primary_key=True)
    plano_id = db.Column(db.Integer, db.ForeignKey("planos.id"))
    modulo_id = db.Column(db.Integer, db.ForeignKey("modulos.id"))

    plano = db.relationship("Plano", back_populates="modulos")
    modulo = db.relationship("Modulo", back_populates="planos")