# Architecture du Projet - Analyse des Ventes PME

## Vue d'ensemble
Architecture à deux services pour l'analyse des ventes d'une PME.

## Services

### 1. Service Scripts (python-scripts)
- **Nom** : `python-scripts`
- **Objectif** : Exécution des scripts Python pour l'import et l'analyse des données
- **Image de base** : `python:3.11-slim`
- **Port exposé** : Aucun (service interne)
- **Fonctionnalités** :
  - Import des données CSV (magasins, produits, ventes)
  - Détection et gestion des doublons
  - Exécution des requêtes SQL d'analyse
  - Stockage des résultats

### 2. Service Database (sqlite-db)
- **Nom** : `sqlite-db`
- **Objectif** : Stockage des données en base SQLite3
- **Image de base** : `alpine:latest` avec SQLite3
- **Port exposé** : Aucun (service interne)
- **Fonctionnalités** :
  - Base de données SQLite3
  - Stockage des données des ventes
  - Stockage des résultats d'analyses

## Communication entre services

```
python-scripts ──(lecture/écriture)──> sqlite-db
     │                    │
     │                    │
     └── Volume partagé ──┘
```

- **Volume partagé** : `/data` pour partager la base de données SQLite
- **Ports exposés** : Aucun (services internes uniquement)
- **Sens de communication** : 
  - python-scripts → sqlite-db (lecture/écriture via volume)
  - sqlite-db → python-scripts (lecture via volume)
- **Protocole** : Accès direct aux fichiers via volume Docker

## Structure des fichiers

```
WildCode/
├── docker-compose.yml
├── Dockerfile
├── scripts/
│   ├── main.py
│   ├── database.py
│   ├── import_data.py
│   └── analysis.py
├── data/
│   └── ventes.db (créé automatiquement)
├── csv/
│   ├── magasins.csv
│   ├── produits.csv
│   └── ventes.csv
└── results/
    └── analyses.sql
```

## Flux de données

1. **Initialisation** : Création des tables SQLite
2. **Import** : Lecture des fichiers CSV et insertion en base
3. **Analyse** : Exécution des requêtes SQL d'analyse
4. **Stockage** : Sauvegarde des résultats d'analyse

## Dépendances

- Service `sqlite-db` démarre en premier
- Service `python-scripts` attend que `sqlite-db` soit prêt
- Volume `/data` partagé entre les deux services
