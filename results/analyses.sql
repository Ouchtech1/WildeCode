-- Script SQL pour les analyses des ventes PME

-- ==============================================
-- REQUÊTE 1: CHIFFRE D'AFFAIRES TOTAL
-- ==============================================

SELECT 
    SUM(Montant_Total) as CA_Total,
    COUNT(*) as Nombre_Ventes,
    MIN(Date) as Date_Debut,
    MAX(Date) as Date_Fin,
    ROUND(AVG(Montant_Total), 2) as Panier_Moyen
FROM VENTE;

-- ==============================================
-- REQUÊTE 2: VENTES PAR PRODUIT
-- ==============================================

SELECT 
    p.ID_Reference,
    p.Nom,
    p.Prix as Prix_Unitaire,
    SUM(v.Quantite) as Quantite_Totale,
    SUM(v.Montant_Total) as CA_Produit,
    COUNT(v.ID_Vente) as Nombre_Ventes,
    ROUND(SUM(v.Montant_Total) / SUM(v.Quantite), 2) as Prix_Moyen_Vendu
FROM PRODUIT p
LEFT JOIN VENTE v ON p.ID_Reference = v.ID_Reference_Produit
GROUP BY p.ID_Reference, p.Nom, p.Prix
ORDER BY CA_Produit DESC;

-- ==============================================
-- REQUÊTE 3: VENTES PAR RÉGION
-- ==============================================

SELECT 
    m.Region,
    COUNT(DISTINCT m.ID_Magasin) as Nombre_Magasins,
    SUM(v.Montant_Total) as CA_Region,
    COUNT(v.ID_Vente) as Nombre_Ventes,
    SUM(v.Quantite) as Quantite_Totale,
    ROUND(SUM(v.Montant_Total) / COUNT(DISTINCT m.ID_Magasin), 2) as CA_Par_Magasin
FROM MAGASIN m
LEFT JOIN VENTE v ON m.ID_Magasin = v.ID_Magasin
GROUP BY m.Region
ORDER BY CA_Region DESC;

-- ==============================================
-- REQUÊTES COMPLÉMENTAIRES
-- ==============================================

-- Top 5 des magasins par CA
SELECT 
    m.ID_Magasin,
    m.Ville,
    m.Region,
    SUM(v.Montant_Total) as CA_Magasin,
    COUNT(v.ID_Vente) as Nombre_Ventes
FROM MAGASIN m
LEFT JOIN VENTE v ON m.ID_Magasin = v.ID_Magasin
GROUP BY m.ID_Magasin, m.Ville, m.Region
ORDER BY CA_Magasin DESC
LIMIT 5;

-- Évolution des ventes par jour
SELECT 
    Date,
    COUNT(*) as Nombre_Ventes,
    SUM(Montant_Total) as CA_Journalier,
    SUM(Quantite) as Quantite_Totale
FROM VENTE
GROUP BY Date
ORDER BY Date;

-- Analyse des stocks vs ventes
SELECT 
    p.ID_Reference,
    p.Nom,
    p.Stock,
    SUM(v.Quantite) as Quantite_Vendue,
    ROUND((SUM(v.Quantite) * 100.0 / p.Stock), 2) as Pourcentage_Stock_Vendu
FROM PRODUIT p
LEFT JOIN VENTE v ON p.ID_Reference = v.ID_Reference_Produit
GROUP BY p.ID_Reference, p.Nom, p.Stock
ORDER BY Pourcentage_Stock_Vendu DESC;
