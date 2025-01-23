# utiliser une image officielle de Python comme base
FROM python:3.12-slim

# définir le répertoire de travail
WORKDIR /app

# copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# copier le contenu du répertoire local dans le répertoire de travail
COPY . .

# Eposer le port par défaut de Django
EXPOSE 8000

# Commande de démarrage par défaut pour un projet Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
