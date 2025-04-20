from datetime import datetime
from models import db

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
