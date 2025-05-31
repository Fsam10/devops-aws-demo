# Etapes du DockerFile
# 1. Utilise une image Python légère et stable
FROM python:3.11-slim

# 2. Crée le dossier de l'app dans le conteneur
WORKDIR /app

# 3. Copie les fichiers requis dans le conteneur
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 4. Définit la variable d'environnement pour Flask
ENV FLASK_APP=app.py

# 5. Port exposé pour la communication (optionnel mais bonne pratique)
EXPOSE 5000

# 6. Commande de démarrage
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
