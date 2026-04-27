# 🐶 Refuge animalier connecté

## 📝 Présentation
Application web Django pour la gestion d'un refuge animalier connecté.

Le projet contient plusieurs apps:
- `accounts` (authentification, profil)
- `core` (pièces, appareils, attributs, historique)
- `gestion`
- `rapports`

## ✅ Prérequis
- Linux (commandes ci-dessous: Ubuntu/Debian)
- Accès terminal
- `git` (optionnel)

## 🐍 Installation de Python et outils (Linux)
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

Vérifier:
```bash
python3 --version
pip3 --version
```

## 📦 Installation du projet
Depuis le dossier du projet (`Refu5Ge`):

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install "django==6.0.4"
```

## 🗄️ Initialiser la base de données (tables + données de migration)
Appliquer toutes les migrations:

```bash
python3 manage.py migrate
```

Voir l'état des migrations:
```bash
python3 manage.py showmigrations
```

## ▶️ Lancer l'application
```bash
python3 manage.py runserver
```

Ouvrir ensuite:
- `http://127.0.0.1:8000/`

## 👤 (Optionnel) Créer un compte admin
```bash
python3 manage.py createsuperuser
```

## 🔁 Commandes utiles
Créer de nouvelles migrations après modification des modèles:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Réinitialiser rapidement la base SQLite locale:
```bash
rm db.sqlite3
python3 manage.py migrate
```

## 📁 Structure rapide
- `Refu5Ge/settings.py`: configuration Django
- `core/models.py`: modèles principaux
- `templates/`: templates HTML
- `static/`: CSS, JS, images
