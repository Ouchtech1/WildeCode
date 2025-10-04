# Modèle Conceptuel de Données (MCD) - Analyse des Ventes PME

## Entités principales

### 1. MAGASIN
- **ID_Magasin** (PK) : INTEGER - Identifiant unique du magasin
- **Ville** : TEXT - Nom de la ville
- **Nombre_Salaries** : INTEGER - Nombre de salariés du magasin
- **Region** : TEXT - Région française (calculée)

### 2. PRODUIT
- **ID_Reference** (PK) : TEXT - Référence unique du produit
- **Nom** : TEXT - Nom du produit
- **Prix** : REAL - Prix unitaire du produit
- **Stock** : INTEGER - Quantité en stock

### 3. VENTE
- **ID_Vente** (PK) : INTEGER - Identifiant unique de la vente (auto-incrémenté)
- **Date** : TEXT - Date de la vente (format YYYY-MM-DD)
- **ID_Reference_Produit** (FK) : TEXT - Référence du produit vendu
- **Quantite** : INTEGER - Quantité vendue
- **ID_Magasin** (FK) : INTEGER - Identifiant du magasin
- **Montant_Total** : REAL - Montant total de la vente

### 4. ANALYSE_RESULTATS
- **ID_Analyse** (PK) : INTEGER - Identifiant unique de l'analyse
- **Type_Analyse** : TEXT - Type d'analyse (CA_TOTAL, VENTES_PRODUIT, VENTES_REGION)
- **Date_Analyse** : TEXT - Date de l'analyse
- **Resultat** : TEXT - Résultat de l'analyse
- **Valeur_Numerique** : REAL - Valeur numérique du résultat

## Relations

```
MAGASIN (1) ──── (N) VENTE
PRODUIT (1) ──── (N) VENTE
```

- Un magasin peut avoir plusieurs ventes
- Un produit peut être vendu plusieurs fois
- Chaque vente appartient à un seul magasin et concerne un seul produit

## Contraintes et règles métier

1. **Clés primaires** : Toutes les entités ont une clé primaire unique
2. **Clés étrangères** : 
   - VENTE.ID_Reference_Produit → PRODUIT.ID_Reference
   - VENTE.ID_Magasin → MAGASIN.ID_Magasin
3. **Contraintes de données** :
   - Prix > 0
   - Quantite > 0
   - Stock >= 0
   - Date au format valide
4. **Calculs automatiques** :
   - Montant_Total = Quantite × Prix
   - Region calculée à partir de Ville

## Mapping des régions françaises

```python
REGIONS = {
    'Paris': 'Île-de-France',
    'Marseille': 'Provence-Alpes-Côte d\'Azur',
    'Lyon': 'Auvergne-Rhône-Alpes',
    'Bordeaux': 'Nouvelle-Aquitaine',
    'Lille': 'Hauts-de-France',
    'Nantes': 'Pays de la Loire',
    'Strasbourg': 'Grand Est'
}
```

## Index recommandés

- INDEX sur VENTE.Date
- INDEX sur VENTE.ID_Magasin
- INDEX sur VENTE.ID_Reference_Produit
- INDEX sur ANALYSE_RESULTATS.Type_Analyse
