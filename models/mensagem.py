from datetime import datetime
from models import db

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