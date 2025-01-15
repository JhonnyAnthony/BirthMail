import os 
from datetime import datetime
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'venv', '.env')
load_dotenv(dotenv_path)

email_group = ['jhonny.souza@fgmdentalgroup.com']
date = datetime.now()
host = os.getenv("HOST")
scope = os.getenv("SCOPE")
today = date.strftime("%d/%m/%Y")
tenant_id = os.getenv("TENANT_ID")
client_id = os.getenv("CLIENT_ID")
email_from = os.getenv("USER_MAIL")
username_guest = os.getenv("USER_GUEST")
client_secret = os.getenv("CLIENT_SECRET")
password_guest = os.getenv("PASSWORD_GUEST")