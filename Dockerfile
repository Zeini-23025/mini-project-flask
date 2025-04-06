# Utilise une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirement.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirement.txt

# Copier le reste de l'application
COPY . .

# Exposer le port utilisé par Flask (par défaut : 5000)
EXPOSE 5000

# Lancer l'application Flask
CMD ["python", "man.py"]
