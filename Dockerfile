# Utiliser une image officielle de Python comme base
FROM python:3.12-slim

# Mettre à jour les paquets et installer psql (client PostgreSQL)
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python listées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du projet dans le conteneur
COPY . .

# Rendre le script wait-for-postgres.sh exécutable
RUN chmod +x wait-for-postgres.sh

# Exposer le port 8000 pour le serveur Django
EXPOSE 8000

# Commande de démarrage par défaut
CMD ["sh", "-c", "./wait-for-postgres.sh db python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]