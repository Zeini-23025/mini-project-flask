# Mini Projet Flask

Cette application web est développée avec **Flask** et **SQLite** pour la gestion des interventions techniques entre des intervenants et des clients.


## 🚀 Technologies utilisées

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- Plotly (pour les graphiques)
- HTML/CSS avec Jinja2 (Templates)
- Docker (optionnel)

---



## 🛠 Fonctionnalités

- Authentification (Login, Signup)
- Gestion des Intervenants (Ajouter, Modifier, Supprimer, Lister)
- Gestion des Clients (Ajouter, Modifier, Supprimer, Lister)
- Gestion des Interventions (Ajouter, Modifier, Supprimer, Lister)
- Visualisation des statistiques avec **Plotly** (interventions réalisées/en attente, répartition par intervenant)

## 🗃️ Structure du projet

```
.
├── Dockerfile
├── instance/
├── main.py
├── requirement.txt
├── static/
├── templates/
└── README.md
```

---

## 📊 Visualisation

La route `/Intervention` affiche deux graphiques générés avec **Plotly** :
- Répartition des interventions **réalisées** par intervenant.
- Répartition des interventions selon l’**état** (réalisée / en attente).

## 📦 Endpoints Principaux

### 🔸 Pages générales

| Route | Description |
|-------|-------------|
| `/` | Page de connexion |
| `/signup` | Page d'inscription |
| `/logout` | Déconnexion |
| `/homme` | Accueil après login |

### 🔸 Intervenants

| Route | Méthode | Description |
|-------|---------|-------------|
| `/Intervenant` | GET | Liste des intervenants |
| `/add_intervenant` | POST | Ajouter un intervenant |
| `/edit_intervenant/<id>` | GET/POST | Modifier un intervenant |
| `/delete_intervenant/<id>` | GET/POST | Supprimer un intervenant |

### 🔸 Clients

| Route | Méthode | Description |
|-------|---------|-------------|
| `/clients` | GET | Liste des clients |
| `/add_client` | POST | Ajouter un client |
| `/edit_client/<id>` | GET/POST | Modifier un client |
| `/delete_client/<id>` | GET/POST | Supprimer un client |

### 🔸 Interventions

| Route | Méthode | Description |
|-------|---------|-------------|
| `/Intervention` | GET | Liste des interventions + Graphiques |
| `/add_intervention` | POST | Ajouter une intervention |
| `/edit_intervention/<id>` | GET/POST | Modifier une intervention |
| `/delete_intervention/<id>` | GET/POST | Supprimer une intervention |

---


## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/Zeini-23025/mini-project-flask.git
cd mini-project-flask
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirement.txt
```

### 4. Lancer l'application

```bash
python main.py
```

L'application sera accessible sur [http://localhost:5000](http://localhost:5000)

---

## 🐳 Docker (optionnel)

Pour exécuter le projet dans un conteneur Docker :

```bash
docker build -t flask-intervention .
docker run -p 5000:5000 flask-intervention
```

---

## 🧪 Accès rapide

- Page de login: `/`
- Signup: `/signup`
- Tableau de bord: `/homme`
- Liste des clients: `/clients`
- Liste des intervenants: `/Intervenant`
- Liste des interventions: `/Intervention`

## 📊 Graphiques

Deux graphiques interactifs sont générés avec Plotly :
- Répartition des interventions **réalisées** par intervenant
- Proportion d’interventions **réalisées** vs **en attente**

---

© Zeiny - Mini Projet Flask