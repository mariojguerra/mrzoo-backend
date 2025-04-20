from models import db

class Raca(db.Model):
    __tablename__ = 'racas'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    especie_id = db.Column(db.Integer, db.ForeignKey('especies.id'), nullable=False)
    animais = db.relationship('Animal', backref='raca_obj', lazy=True)
