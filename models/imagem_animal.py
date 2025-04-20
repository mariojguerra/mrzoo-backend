from datetime import datetime
from models import db

class ImagemAnimal(db.Model):
    __tablename__ = 'imagens_animais'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)

    def to_json(self):
        return {
            "id": self.id,
            "animal_id": self.animal_id,
            "url": self.url,
            "data_upload": self.data_upload.isoformat()
        }