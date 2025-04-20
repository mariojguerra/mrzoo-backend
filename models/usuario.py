from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import relationship
from models import db

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