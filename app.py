from flask import Flask, jsonify, request, make_response,redirect, url_for,abort
from flask_restful import Api, Resource
import jwt
from DbManager import MSSQL,DashLog
import json

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
    ''' print(request.environ)
        Reha ruft in der Datenbank authapi den App Secret Key ab.
        --> Die Anwendung Reha sendet den App Secret Key zusammen mit der WindowsKennung verschlüsselt mit JWT an die AuthApi App.
        --> Dort wird der JWT Token entschlüsselt
        --> Der App Secret Key wird gegengeprüft, ob dieser in der authapi Datenbank steht.
        --> Falls ja --> Werden die Berechtigungen der App Reha abgefragt und zurück an die App Reha gesendet
        --> Falls nein --> es werden keine Berechtigungen zurück geschickt.'''
        
        
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

@app.route('/get_permissionsTeam', methods=['GET'])
def get_permissions():
    #encode = jwt.encode({"user":"sbl2933"},"wurstwasser","HS256")

    return jsonify({"dwa1":"dwad1"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)