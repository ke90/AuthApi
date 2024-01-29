from flask import Flask, jsonify, request, make_response,redirect, url_for,abort
from flask_restful import Api, Resource
import jwt
from DbManager import MSSQL,DashLog
import json


    # '''Reha ruft in der Datenbank authapi den App Secret Key ab.
    #     --> Die Anwendung Reha sendet den App Secret Key zusammen mit der WindowsKennung verschlüsselt mit JWT an die AuthApi App.
    #     --> Dort wird der JWT Token entschlüsselt
    #     --> Der App Secret Key wird gegengeprüft, ob dieser in der authapi Datenbank steht.
    #     --> Falls ja --> Werden die Berechtigungen der App Reha abgefragt und zurück an die App Reha gesendet
    #     --> Falls nein --> es werden keine Berechtigungen zurück geschickt.'''

app = Flask(__name__)
connection = MSSQL()
dl = DashLog()


#TODO
# ARCHIV! WIRD NOCH UMGEBAUT
# def verifyToken():
#     if not request.cookies.get('api_token'):
#         print("User nicht authentifiziert --> Starte Authentifizierung")
#         print(request.endpoint)
#         return redirect(url_for('authenticate',next=request.endpoint))
#     else:
#         print("Token wurde erstellt...")
        
#     return True

def checkToken(token):
    decoded_token = None
    try:
        decoded_token = jwt.decode(token,"wurstwasser","HS256")
        return decoded_token
    except:
        dl.send_log(2,'Fehlerhafter Token')
        return abort(403)

@app.route('/authenticate', methods=['GET'])
def authenticate():
    print("Authenticate")
    # response = app.response_class(response=redirect('/get_permissionUser'), status=302)
    next_url = request.args.get('next')
    print(next_url)
    response = make_response(redirect(next_url))
    encode = jwt.encode({"user":"sbl2933", "permission":['admin']},"wurstwasser","HS256")
    response.set_cookie('api_token',encode)
    return response
    # jwt.encode()



@app.route('/get_permissionUser', methods=['GET'])
def get_permissionUser():        
        
    if not request.cookies.get('api_token'):
        print("User nicht authentifiziert --> Starte Authentifizierung")
        return redirect(url_for('authenticate',next=request.endpoint))
    else:
        print("Token wurde erstellt...")
        
    token = request.cookies.get('api_token')
    valid = checkToken(token)

    if valid:
        sql = '''SELECT * FROM testtbl2'''
        data = connection.get_queried_data(True,sql)
        response = app.response_class(response=json.dumps(data), status=200, mimetype='application/json')
        return response
    else:
        abort(403)

        

    # Parameter: JWT Token + App ID
    # -> mit der App ID wird in der Authapi Datenbank der SecretKey der App abgefragt
    # -> Das JWT Token wird mit dem SecretKey dekodiert.
    # -> Bei erfolgreichem dekodieren werden die Berechtigungen des Users aus der DB abgefragt und zurückgegeben
    # -> Bei nicht erfolgreichem dekodieren -> 403
@app.route('/getPermissions', methods=['GET'])
def getPermissions():

    # JWT Token aus dem Header abrufen
    token = request.headers.get('Authorization')
    if not token:
        abort(403, description="JWT Token is missing")

    # App-ID aus dem Query-String-Parameter abrufen
    app_id = request.args.get('appID')
    if not app_id:
        abort(400, description="App ID is missing")

    print("-------In app.py")
    print(app_id)
    print(token)
    params = [app_id]

    sql = '''SELECT id,appname,secretkey FROM apps WHERE id = 1'''
    authdata = connection.get_queried_data(True,sql)
    print(authdata)
    if authdata[0]['secretkey']:
        decoded_token = jwt.decode(token,authdata[0]['secretkey'],"HS256")

        if decoded_token:
            params = params + decoded_token['windows_login']

            sql = '''SELECT windows_kennung, permission, appname, secretkey FROM permission_zuordnung
                        INNER JOIN permissions p ON p.id = permission_zuordnung.permission_id
                        INNER JOIN apps a ON a.id = p.app_id WHERE p.app_id = %s AND windows_kennung = %s'''
            permissions = connection.get_queried_data(True,sql,params)
            response = app.response_class(response=json.dumps(permissions), status=200, mimetype='application/json')
            return response
        else:
            abort(403)
    else:
        abort(501)

@app.route('/getPermissions1', methods=['GET'])
def getPermissions1():
    sql = '''SELECT * FROM apps'''
    data = connection.get_queried_data(True,sql)
    response = app.response_class(response=json.dumps(data), status=200, mimetype='application/json')
    return response

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)