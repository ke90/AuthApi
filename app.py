from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import jwt
from DbManager import MSSQL

app = Flask(__name__)
connection = MSSQL()


@app.route('/get_permissionUser/', methods=['GET'])
def get_permissionUser():
    
    sql = '''SELECT * FROM testtbl'''
    data = connection.get_queried_data(True,sql)
    
    #print(request.environ)
    # Reha ruft in der Datenbank authapi den App Secret Key ab.
    # --> Die Anwendung Reha sendet den App Secret Key zusammen mit der WindowsKennung verschlüsselt mit JWT an die AuthApi App.
    # --> Dort wird der JWT Token entschlüsselt
    # --> Der App Secret Key wird gegengeprüft, ob dieser in der authapi Datenbank steht.
    # --> Falls ja --> Werden die Berechtigungen der App Reha abgefragt und zurück an die App Reha gesendet
    # --> Falls nein --> es werden keine Berechtigungen zurück geschickt.
    
    # return jsonify({"test":'test'})
    return jsonify(data)

def get_permissions():

    #encode = jwt.encode({"user":"sbl2933"},"wurstwasser","HS256")


    # TODO
    # User ruft im Browser die URL auf.
    # Es wird ein JWT Token generiert mit dem Windowslogin
    # Dieser wird an das Frontend zurückgegeben und im LocalStorageg gespeichert. Das Frontend zeigt "Weiterleitung an." Der JWT Token im LocalStorage wird an eine neue Route im Backend gesendet 
    # Dort wird der Token decodiert und man erhält den WindowsLogin. 
    # In der Funktion wird nun geprüft, über die Datenbank "authapi" ob der WindowsUser aus dem Token die Berechtigung hat, die Berechtigungen aus der Datenbank zusehen.*args
    # Bei Ja werden die Berechtigungen zurückgegeben.
    # Hintergrund dieser Methode: Der User könnte eventuell den WindowsLogin Clientseitig manipulieren. Somit könnte er nach der aktuellen Methode die Berechtigungen von anderen WindowsUsers ausgegeben bekommen.
    

    # Vorerst:
    # Beim Aufruf der URL wird der WindowsUser ausgelesen
    # Das Backend prüft in der "authapi" Datenbank, ob der WindowsUser die Berechtigung besitzt die Berechtigungen zu sehen.*args
    # Falls Ja --> werden diese zurückgegeben

    return jsonify({})
    #return jsonify({"token":encode})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    #app.run(debug=True)