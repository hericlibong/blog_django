# Utiliser une image officielle de Python comme base
FROM python:3.12-slim

# Installer le client PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# 1) On place notre répertoire de travail “temporaire” à /app
WORKDIR /app

# 2) On copie le requirements.txt et on installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) On copie tout le projet (blog_django/*) dans /app
COPY . .

# 4) Rendre le script d’attente exécutable
RUN chmod +x wait-for-postgres.sh

# 5) IMPORTANT : on redéfinit le WORKDIR pour pointer vers le répertoire 
#    qui contient manage.py, c’est-à-dire /app/django_blog
WORKDIR /app/django_blog

# 6) On expose le port
EXPOSE 8000

# 7) Commande de démarrage par défaut
CMD ["sh", "-c", "../wait-for-postgres.sh db python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
