import logging 
import requests
from sendMail import SendMail
from config import client_secret, client_id, tenant_id, scope
scope = 'https://graph.microsoft.com/.default'

def getManager(): 
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token' # End-point for token retrieval
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    access_token = response.json().get('access_token')
    
    # Fetch manager information
    user_id = 'd602bd3e-6752-4b4a-9dc0-c7ab6020f2d3'
    url = f'https://graph.microsoft.com/v1.0/users/{self.nomeUsuario}@fgmdentalgroup.com/manager'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if (response.status_code == 200):
        item_details = response.json()
        emailSuperior = item_details.get('mail')
        print(emailSuperior)

if __name__ == "__main__":
    getManager()
