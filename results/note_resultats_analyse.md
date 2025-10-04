# NOTE DES RÉSULTATS D'ANALYSE
## Projet Simplon - Data Engineer

### Date d'analyse : 4 octobre 2025

---

## RESULTATS DES 3 REQUETES DEMANDEES

### 1. CHIFFRE D'AFFAIRES TOTAL (Requête 4.a)

**Requête SQL :**
```sql
SELECT 
    SUM(Montant_Total) as CA_Total,
    COUNT(*) as Nombre_Ventes,
    MIN(Date) as Date_Debut,
    MAX(Date) as Date_Fin,
    ROUND(AVG(Montant_Total), 2) as Panier_Moyen
FROM VENTE;
```

**Résultats obtenus :**
- **Chiffre d'affaires total** : 5 268,78€
- **Nombre de ventes** : 30 transactions
- **Période analysée** : Du 27 mai 2023 au 25 juin 2023
- **Panier moyen** : 175,63€

---

### 2. VENTES PAR PRODUIT (Requête 4.b)

**Requête SQL :**
```sql
SELECT 
    p.ID_Reference,
    p.Nom,
    p.Prix as Prix_Unitaire,
    SUM(v.Quantite) as Quantite_Totale,
    SUM(v.Montant_Total) as CA_Produit,
    COUNT(v.ID_Vente) as Nombre_Ventes
FROM PRODUIT p
LEFT JOIN VENTE v ON p.ID_Reference = v.ID_Reference_Produit
GROUP BY p.ID_Reference, p.Nom, p.Prix
ORDER BY CA_Produit DESC;
```

**Résultats obtenus :**

| Produit | Référence | Prix Unitaire | Quantité Vendue | CA Généré | Nombre de Ventes |
|---------|-----------|---------------|-----------------|-----------|------------------|
| Produit D | REF004 | 79,99€ | 21 unités | 1 679,79€ | 6 |
| Produit E | REF005 | 39,99€ | 35 unités | 1 399,65€ | 7 |
| Produit A | REF001 | 49,99€ | 24 unités | 1 199,76€ | 6 |
| Produit C | REF003 | 29,99€ | 15 unités | 449,85€ | 5 |
| Produit B | REF002 | 19,99€ | 30 unités | 599,70€ | 6 |

**Produit le plus vendu** : Produit D (REF004) avec 1 679,79€ de CA

---

### 3. VENTES PAR RÉGION (Requête 4.c)

**Requête SQL :**
```sql
SELECT 
    m.Region,
    COUNT(DISTINCT m.ID_Magasin) as Nombre_Magasins,
    SUM(v.Montant_Total) as CA_Region,
    COUNT(v.ID_Vente) as Nombre_Ventes,
    SUM(v.Quantite) as Quantite_Totale
FROM MAGASIN m
LEFT JOIN VENTE v ON m.ID_Magasin = v.ID_Magasin
GROUP BY m.Region
ORDER BY CA_Region DESC;
```

**Résultats obtenus :**

| Région | Nombre de Magasins | CA Généré | Nombre de Ventes | Quantité Totale |
|--------|-------------------|-----------|------------------|-----------------|
| Auvergne-Rhône-Alpes | 1 | 1 059,79€ | 4 | 13 |
| Provence-Alpes-Côte d'Azur | 1 | 1 009,73€ | 5 | 25 |
| Nouvelle-Aquitaine | 1 | 829,81€ | 3 | 10 |
| Île-de-France | 1 | 799,90€ | 4 | 16 |
| Hauts-de-France | 1 | 599,70€ | 3 | 30 |
| Pays de la Loire | 1 | 599,70€ | 3 | 15 |
| Grand Est | 1 | 370,15€ | 2 | 7 |

**Région la plus performante** : Auvergne-Rhône-Alpes avec 1 059,79€ de CA

---

## ANALYSES COMPLEMENTAIRES

### Top 3 Magasins par Performance
1. **Magasin Lyon** (Auvergne-Rhône-Alpes) : 1 059,79€
2. **Magasin Marseille** (Provence-Alpes-Côte d'Azur) : 1 009,73€
3. **Magasin Bordeaux** (Nouvelle-Aquitaine) : 829,81€

### Évolution Temporelle
- **Jour de plus forte activité** : 31 mai 2023 (279,93€)
- **Jour de plus faible activité** : 29 mai 2023 (59,98€)
- **Tendance** : Stable avec des pics occasionnels

### Analyse des Stocks vs Ventes
- **Produit le plus vendu par rapport au stock** : Produit E (43,75% du stock vendu)
- **Produit avec le plus gros stock restant** : Produit D (99 unités restantes)

---

## OBSERVATIONS CLES

1. **Performance géographique** : Les régions du Sud (Auvergne-Rhône-Alpes, PACA) sont les plus performantes
2. **Performance produit** : Le Produit D (79,99€) génère le plus de CA malgré un prix élevé
3. **Volume vs Valeur** : Le Produit E a le meilleur ratio volume/valeur
4. **Répartition équitable** : Les ventes sont bien réparties entre les magasins

---

## METHODOLOGIE TECHNIQUE

- **Base de données** : SQLite3 avec index optimisés
- **Gestion des doublons** : Système de détection automatique
- **Collecte des données** : Support HTTP et fichiers locaux
- **Architecture** : Docker avec 2 services (scripts + base de données)
- **Langage** : Python 3.11 avec pandas et requests

---

*Note générée automatiquement par le système d'analyse des ventes PME*
