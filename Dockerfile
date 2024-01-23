# Verwenden eines offiziellen Python-Runtime als Eltern-Image
FROM python:3.8-slim

# Setzen des Arbeitsverzeichnisses im Container
WORKDIR /app

# Kopieren der benötigten Dateien in das Container-Verzeichnis
COPY ./requirements.txt ./

# Installieren der benötigten Python-Pakete
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des restlichen App-Codes
COPY . .

# Festlegen des Ports, auf dem die Anwendung laufen wird
EXPOSE 5000

# Definieren des Befehls zum Ausführen der Anwendung
CMD ["python", "./app.py"]
