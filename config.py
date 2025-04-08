# config.py
import os

# Chave secreta
SECRET_KEY = '2404@Theo'

MYSQL_USER = 'root'
MYSQL_PASSWORD = 'hvMYogfEVMNDAKMrrxazEALyySAKgeYU'
MYSQL_HOST = 'mysql.railway.internal'
MYSQL_PORT = 3306
MYSQL_DB = 'railway'

SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

#mysql://root:hvMYogfEVMNDAKMrrxazEALyySAKgeYU@mysql.railway.internal:3306/railway