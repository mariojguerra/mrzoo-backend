from datetime import datetime
from models import db

class Assinatura(db.Model):
    __tablename__ = "assinaturas"
    __table_args__ = {'mysql_charset': 'utf8mb4'}

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
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