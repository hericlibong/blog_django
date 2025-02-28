# My Django Blog

1. **Présentation du projet**
   - Description du portfolio
   - Technologies utilisées
   - Fonctionnalités principales

2. **Installation et configuration**
   - Prérequis
   - Installation avec Docker
   - Configuration des variables d’environnement

3. **Utilisation**
   - Lancement du projet en local
   - Accès à l’application
   - Explication des principales routes et fonctionnalités

4. **Déploiement**
   - Déploiement sur Render
   - Configuration GitHub Actions (CI/CD)

5. **Tests et qualité du code**
   - Exécution des tests
   - Conformité PEP8 avec flake8
   - Couverture des tests

6. **API et chatbot**
   - Présentation du chatbot IA
   - Utilisation de l’API OpenAI

7. **Contributeurs et informations supplémentaires**
   - Comment contribuer au projet
   - Contact et réseaux sociaux

---

### 📌 **1. Présentation du projet**
Nom du projet : **Portfolio de HericLdev**

Ce projet est un portfolio développé avec Django et Bootstrap, permettant d’afficher les projets d’un développeur. Il inclut un assistant IA basé sur l’API OpenAI pour répondre aux questions des visiteurs.

**🛠️ Technologies utilisées :**
- **Backend** : Django 5.1, PostgreSQL, Docker
- **Frontend** : Bootstrap, HTML/CSS
- **Cloud & Stockage** : Cloudinary (médias), Render (hébergement)
- **IA** : OpenAI API (GPT-4o mini)
- **CI/CD** : GitHub Actions

**✨ Fonctionnalités :**
- 🎨 Page de présentation du développeur
- 📂 Listing des projets avec détails et images
- 🔍 Chatbot interactif pour répondre aux questions sur les projets et le profil
- 🌐 Interface responsive avec Bootstrap
- 📷 Gestion des médias sur Cloudinary
- 🚀 Déploiement automatique via Render

---

### 📌 **2. Installation et configuration**
#### **🔧 Prérequis**
Avant de commencer, assure-toi d’avoir :
- Docker et Docker Compose installés
- Un compte sur [OpenAI](https://platform.openai.com/) pour générer une clé API
- Un compte sur [Cloudinary](https://cloudinary.com/) pour stocker les médias

#### **📥 Installation avec Docker**
1. **Cloner le projet :**
   ```sh
   git clone https://github.com/hericlibong/blog_django.git
   cd blog_django
   ```

2. **Configurer les variables d’environnement :**
   Renomme le fichier `.env.sample` en `.env` et renseigne les valeurs :
   ```sh
   cp .env.sample .env
   ```

3. **Lancer le projet avec Docker :**
   ```sh
   docker-compose up --build
   ```

---

### 📌 **3. Utilisation**
#### **🎯 Lancement du projet en local**
Une fois le projet démarré, accède à l’application sur [http://localhost:8000](http://localhost:8000).

#### **🚀 Accès aux principales fonctionnalités :**
- 📋 **Liste des projets** : [http://localhost:8000/portfolio/projects/](http://localhost:8000/portfolio/projects/)
- 🤖 **Chatbot** : [http://localhost:8000/openaichat/chatbot/](http://localhost:8000/openaichat/chatbot/)
- 👤 **Profil** : Affiché dans la sidebar

---

### 📌 **4. Déploiement**
L’application est hébergée sur **Render** avec une pipeline CI/CD sur **GitHub Actions**.

#### **🔹 Déploiement automatique**
À chaque `push` sur `main`, le workflow :
1. **Lance les tests** ✅
2. **Construit l’image Docker** 🛠️
3. **Pousse l’image sur Docker Hub** 🐳
4. **Déploie l’application sur Render** 🚀

#### **🔹 Configuration des secrets GitHub**
Ajoute ces secrets dans **GitHub Actions** (`Settings > Secrets and variables > Actions`) :
- `OPENAI_API_KEY`
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- `DATABASE_URL`

---

### 📌 **5. Tests et qualité du code**
#### **🧪 Exécution des tests**
Lancer tous les tests avec :
```sh
docker-compose run --rm web pytest --cov=openaichat openaichat/tests/test_views.py
```

#### **📏 Conformité PEP8**
Vérifier le style du code avec Flake8 :
```sh
docker-compose run --rm web flake8
```

---

### 📌 **6. API et chatbot**
#### **🤖 Assistant IA**
Le chatbot est basé sur OpenAI et répond aux questions sur :
- 📌 Les projets du portfolio
- 👤 Le profil du développeur
- 🎓 Les compétences et expériences

📡 **Endpoint API** :
```http
POST /openaichat/chatbot-response/
```
📥 **Exemple de requête JSON :**
```json
{
  "message": "Quels sont tes projets ?"
}
```
📤 **Réponse attendue :**
```json
{
  "response": "Voici mes projets : Projet 1, Projet 2..."
}
```

---

### 📌 **7. Contributeurs et informations supplémentaires**
#### **💡 Contribuer au projet**
1. **Forker** le repo
2. **Créer une branche** pour tes modifications :
   ```sh
   git checkout -b feature-ma-fonctionnalite
   ```
3. **Commiter** les changements :
   ```sh
   git commit -m "Ajout de ma fonctionnalité"
   ```
4. **Pousser** la branche et proposer un `Pull Request` :
   ```sh
   git push origin feature-ma-fonctionnalite
   ```

#### **📞 Contact**
- **Portfolio** : [hericldev.onrender.com](https://hericldev.onrender.com)
- **GitHub** : [github.com/hericlibong](https://github.com/hericlibong)

---

✅ **Cette documentation fournit une vue complète de ton projet, et sera utile aux utilisateurs et contributeurs potentiels.** 🚀
