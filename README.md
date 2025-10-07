# Projet d'Analyse des Ventes PME

### Description du Projet

Ce projet consiste à créer un système d'analyse des ventes pour une PME utilisant une architecture Docker à deux services :
- **Service Scripts** : Exécution des scripts Python pour l'import et l'analyse
- **Service Database** : Stockage des données en SQLite3

### Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   python-scripts│    │   sqlite-db     │
│                 │    │                 │
│ - Import CSV    │◄──►│ - Base SQLite   │
│ - Analyses SQL  │    │ - Stockage      │
│ - Gestion doublons│   │ - Persistance   │
└─────────────────┘    └─────────────────┘
         │                       │
         └───── Volume partagé ───┘
```

### Structure du Projet

```
WildCode/
├── docker-compose.yml          # Orchestration des services
├── Dockerfile                  # Image Python
├── requirements.txt            # Dépendances Python
├── architecture.md             # Documentation architecture
├── schema_database.md          # Schéma de base de données
├── scripts/
│   ├── main.py                # Script principal
│   ├── database.py            # Gestion base de données
│   ├── import_data.py          # Import des données CSV
│   └── analysis.py            # Analyses SQL
├── results/
│   ├── analyses.sql            # Requêtes SQL
│   └── rapport_analyse.md     # Rapport des résultats
├── data/                      # Base de données SQLite (créée automatiquement)
├── magasins.csv              # Données des magasins
├── produits.csv              # Données des produits
└── ventes.csv                # Données des ventes
```

### Installation et Exécution

#### Prérequis
- Docker
- Docker Compose

#### Commandes

1. **Cloner le projet**
```bash
git clone [url-du-repo]
cd WildCode
```

2. **Lancer l'architecture complète**
```bash
docker-compose up --build
```

3. **Voir les logs**
```bash
docker-compose logs -f python-scripts
```

4. **Arrêter les services**
```bash
docker-compose down
```

### Fonctionnalités

#### Import des Données
- Import automatique des fichiers CSV
- Gestion des doublons (ventes en temps réel)
- Validation des données
- Calcul automatique des montants

#### Analyses Disponibles
- **Chiffre d'affaires total**
- **Ventes par produit** (classement par CA)
- **Ventes par région** (performance géographique)

#### Analyses Complémentaires
- Top 5 des magasins
- Évolution temporelle des ventes
- Analyse des stocks vs ventes

### Base de Données

#### Tables Principales
- **MAGASIN** : Informations des magasins (ID, Ville, Salariés, Région)
- **PRODUIT** : Catalogue produits (Référence, Nom, Prix, Stock)
- **VENTE** : Transactions (Date, Produit, Quantité, Magasin, Montant)
- **ANALYSE_RESULTATS** : Stockage des résultats d'analyses

#### Relations
```
MAGASIN (1) ──── (N) VENTE
PRODUIT (1) ──── (N) VENTE
```

### Configuration

#### Variables d'Environnement
- `DATABASE_PATH` : Chemin vers la base SQLite (défaut: `/data/ventes.db`)

#### Ports
- Aucun port exposé (services internes uniquement)

### Résultats d'Analyse

Le système génère automatiquement :
1. **Rapport de synthèse** dans les logs
2. **Résultats stockés** en base de données
3. **Requêtes SQL** exportées dans `results/analyses.sql`
4. **Documentation** des résultats dans `results/rapport_analyse.md`

### Développement

#### Ajouter une Nouvelle Analyse
1. Créer une méthode dans `analysis.py`
2. Ajouter l'appel dans `main.py`
3. Stocker le résultat avec `_store_analysis_result()`

#### Modifier le Schéma de Base
1. Modifier `database.py` (méthode `create_tables()`)
2. Mettre à jour `schema_database.md`
3. Reconstruire l'image Docker

### Livrables

- Schéma d'architecture (`architecture.md`)
- Schéma de base de données (`schema_database.md`)
- Dockerfile
- docker-compose.yml
- Scripts d'import et d'analyse
- Requêtes SQL (`results/analyses.sql`)
- Documentation des résultats

### Monitoring

#### Vérifier l'État des Services
```bash
docker-compose ps
```

#### Accéder à la Base de Données
```bash
docker-compose exec sqlite-db sqlite3 /data/ventes.db
```

#### Voir les Résultats d'Analyse
```sql
SELECT * FROM ANALYSE_RESULTATS ORDER BY Date_Analyse DESC;
```

### Dépannage

#### Problèmes Courants
1. **Service ne démarre pas** : Vérifier que le port n'est pas utilisé
2. **Erreur d'import** : Vérifier la présence des fichiers CSV
3. **Base de données corrompue** : Supprimer le volume et relancer

#### Logs Détaillés
```bash
docker-compose logs python-scripts
docker-compose logs sqlite-db
```

### Support

Pour toute question ou problème :
1. Vérifier les logs Docker
2. Consulter la documentation
3. Contacter l'équipe de développement

---
