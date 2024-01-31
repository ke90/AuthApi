import requests
import jwt
import json
from datetime import datetime, timedelta
from DbManager import MSSQL


class PermissionsRequester:
    def __init__(self):
        self.connection = MSSQL()
        self.api_url = 'http://localhost:81/getPermissions'
        self.app_id = 1

    def get_secret_key(self):
        # params = (self.app_id)
        params = {}
        params['APP_ID'] = self.app_id
        # sql = "SELECT secretkey FROM apps WHERE id = %s"
        sql = "SELECT secretkey FROM apps WHERE id = %(APP_ID)s"
        result = self.connection.get_queried_data(True,sql,params)
        print(result)
        return result[0]['secretkey'] if result else None

    def generate_jwt_token(self, windows_login, secret_key):
        payload = {
            'windows_login': windows_login,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload,secret_key, algorithm="HS256")
        #print(token)
        return token

    def get_permissions(self, windows_login):
        secret_key = self.get_secret_key()
        if not secret_key:
            raise Exception("Die App ist nicht vorhanden in der Datenbank")

        token = self.generate_jwt_token(windows_login, secret_key)
        headers = {'Authorization': f'Bearer {token}'}
        
        response = requests.get(self.api_url, headers=headers, params={'appID': self.app_id})

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception(f"Error in request: {response.status_code}")

