# reset_db.py

from app import app
from models import db

if __name__ == "__main__":
    with app.app_context():
        print("🧨 Apagando todas as tabelas...")
        db.drop_all()
        print("✅ Tabelas apagadas.")

        print("🛠️ Criando novas tabelas...")
        db.create_all()
        print("✅ Tabelas criadas com sucesso.")
