from datetime import datetime
from models import db

class Match(db.Model):
    __tablename__ = 'match'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal1_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    animal2_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "animal1_id": self.animal1_id,
            "animal2_id": self.animal2_id,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
