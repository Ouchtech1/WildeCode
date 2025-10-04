# Dockerfile - Service Scripts Python
FROM python:3.11-slim

# Répertoire de travail
WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copie des dépendances Python
COPY requirements.txt .

# Installation des packages Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie des scripts
COPY scripts/ ./scripts/

# Copie des données CSV
COPY *.csv ./

# Création du répertoire de données
RUN mkdir -p /data

# Variable d'environnement base de données
ENV DATABASE_PATH=/data/ventes.db

# Point d'entrée
CMD ["python", "scripts/main.py"]
