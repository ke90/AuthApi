# AuthApi

## Beschreibung

Dieses Projekt ist eine Flask-Api, die eine API bereitstellt, um Berechtigungen für Benutzer basierend auf ihren Windows-Anmeldeinformationen zu verwalten. Die Hauptfunktionen der API umfassen das Generieren eines JWT-Tokens mit dem Windows-Login des Benutzers und das Überprüfen der Berechtigungen dieses Benutzers in der "authapi" Datenbank.

Beispiel Reha:  
Reha ruft in der Datenbank "authapi" den App Secret Key ab. --> Die Anwendung Reha sendet den App Secret Key zusammen mit der WindowsKennung verschlüsselt mit JWT an die AuthApi App. --> Dort wird der JWT Token entschlüsselt --> Der App Secret Key wird gegengeprüft, ob dieser in der authapi Datenbank steht. --> Falls ja --> Werden die Berechtigungen der App Reha abgefragt und zurück an die App Reha gesendet
--> Falls nein --> es werden keine Berechtigungen zurück geschickt.

Hintergrund:
Es soll nur die Applikation auf den URL Pfad zugreifen dürfen, daher wird für jede Applikation ein SECRET KEY in der authapi Datenbank hinterlegt.

## Funktionalitäten

- **JWT-Token-Erstellung**: Generiert einen JWT-Token, der den Windows-Benutzernamen des Benutzers enthält.
- **Berechtigungsüberprüfung**: Überprüft, ob der Benutzer die notwendigen Berechtigungen hat, um auf bestimmte Ressourcen zuzugreifen.

## Installation

Um das Projekt lokal einzurichten, folgen Sie diesen Schritten:

1. Klonen Sie das Repository:
   git clone [URL Ihres Git-Repositorys]

2. Wechseln Sie in das Projektverzeichnis:
   cd [Projektverzeichnis]

3. Erstellen Sie eine virtuelle Umgebung:
   python -m venv venv

4. Aktivieren Sie die virtuelle Umgebung:

- Windows:
  ```
  .\venv\Scripts\activate
  ```
- Unix oder MacOS:
  ```
  source venv/bin/activate
  ```

5. Installieren Sie die erforderlichen Pakete:

## Ausführung

Starten Sie die Anwendung mit:
flask run
