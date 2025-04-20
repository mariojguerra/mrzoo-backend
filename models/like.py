from models import db

class Like(db.Model):
    __tablename__ = 'like'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    liked_animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "animal_id": self.animal_id,
            "liked_animal_id": self.liked_animal_id
        }