import os
from decouple import config

os.environ['SSH_HOST'] = "ssh.pythonanywhere.com"
os.environ['SSH_USERNAME'] = "Pentagruel"
os.environ['SSH_PASSWORD'] = "(US)ue%1"
os.environ['REMOTE_BIND_ADDRESS'] = 'pentagruel.mysql.pythonanywhere-services.com'
os.environ['REMOTE_PORT_ADDRESS'] = '3306'
os.environ['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://Pentagruel:(US)ue%1@127.0.0.1:{}/Pentagruel$staging-bullionsniper"
os.environ['SSH_TIMEOUT'] = '3600.0'
os.environ['TUNNEL_TIMEOUT'] = '3600.0'

