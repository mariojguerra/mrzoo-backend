# config.py

SECRET_KEY = '2404@Theo'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'hvMYogfEVMNDAKMrrxazEALyySAKgeYU'
MYSQL_HOST = 'caboose.proxy.rlwy.net'
MYSQL_PORT = 43162
MYSQL_DB = 'railway'
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

#mysql://root:hvMYogfEVMNDAKMrrxazEALyySAKgeYU@mysql.railway.internal:3306/railway
#mysql://root:hvMYogfEVMNDAKMrrxazEALyySAKgeYU@caboose.proxy.rlwy.net:43162/railway
