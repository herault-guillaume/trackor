import os

os.environ['APP_KEY'] = 'mysecretkey'

os.environ['MAIL_SERVER'] = 'ssl0.ovh.net'
os.environ['MAIL_PORT'] = '465'
os.environ['MAIL_USERNAME'] = 'noreply@bullion-sniper.fr'
os.environ['MAIL_PASSWORD'] = '(US)ue%1(US)ue%1'
os.environ['MAIL_USE_TLS'] = '0'
os.environ['MAIL_USE_SSL'] = '1'

os.environ['SSH_HOST'] = "ssh.pythonanywhere.com"
os.environ['SSH_USERNAME'] = "Pentagruel"
os.environ['SSH_PASSWORD'] = "(US)ue%1"
os.environ['REMOTE_BIND_ADDRESS'] = 'pentagruel.mysql.pythonanywhere-services.com'
os.environ['REMOTE_PORT_ADDRESS'] = '3306'
os.environ['DATABASE_URL'] = "mysql+mysqlconnector://Pentagruel:(US)ue%1@127.0.0.1:{}/Pentagruel$bullionsniper"
os.environ['SSH_TIMEOUT'] = '3600.0'
os.environ['TUNNEL_TIMEOUT'] = '3600.0'