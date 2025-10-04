#!/usr/bin/env python3
"""
Import des données CSV avec gestion des doublons
"""

import pandas as pd
import sqlite3
import requests
from datetime import datetime
from typing import List, Tuple
from database import DatabaseManager

class DataImporter:
    """Gestionnaire d'import des données CSV"""
    
    def __init__(self, db_manager: DatabaseManager, use_http: bool = False, base_url: str = "http://localhost:8000"):
        """
        Initialise l'importeur de données
        
        Args:
            db_manager: Instance du gestionnaire de base de données
            use_http: Utiliser la collecte HTTP (défaut: False)
            base_url: URL de base pour la collecte HTTP
        """
        self.db_manager = db_manager
        self.use_http = use_http
        self.base_url = base_url
        
    def _collect_csv_via_http(self, filename: str) -> bool:
        """
        Collecte un fichier CSV via HTTP
        
        Args:
            filename: Nom du fichier à télécharger
            
        Returns:
            bool: True si le téléchargement a réussi
        """
        if not self.use_http:
            return True
            
        url = f"{self.base_url}/{filename}"
        print(f"Collecte HTTP de {filename} depuis {url}...")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
                
            print(f"{filename} collecté via HTTP ({len(response.content)} bytes)")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur collecte HTTP de {filename}: {e}")
            return False
        except Exception as e:
            print(f"Erreur inattendue pour {filename}: {e}")
            return False
        
    def import_magasins(self, csv_file: str = "magasins.csv"):
        """
        Importe les données des magasins
        
        Args:
            csv_file: Chemin vers le fichier CSV des magasins
        """
        print(f"Import des magasins depuis {csv_file}...")
        
        # Collecter le fichier via HTTP si nécessaire
        if not self._collect_csv_via_http(csv_file):
            print(f"Impossible de collecter {csv_file} via HTTP")
            return
        
        try:
            # Lire le fichier CSV
            df = pd.read_csv(csv_file)
            
            # Renommer les colonnes pour correspondre à notre schéma
            df.columns = ['ID_Magasin', 'Ville', 'Nombre_Salaries']
            
            # Ajouter la colonne Région
            df['Region'] = df['Ville'].apply(self.db_manager.get_region_from_city)
            
            # Insérer les données
            cursor = self.db_manager.connection.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO MAGASIN 
                    (ID_Magasin, Ville, Nombre_Salaries, Region)
                    VALUES (?, ?, ?, ?)
                """, (row['ID_Magasin'], row['Ville'], 
                     row['Nombre_Salaries'], row['Region']))
            
            self.db_manager.connection.commit()
            print(f"{len(df)} magasins importés avec succès")
            
        except Exception as e:
            print(f"Erreur lors de l'import des magasins: {e}")
            self.db_manager.connection.rollback()
            raise
    
    def import_produits(self, csv_file: str = "produits.csv"):
        """
        Importe les données des produits
        
        Args:
            csv_file: Chemin vers le fichier CSV des produits
        """
        print(f"Import des produits depuis {csv_file}...")
        
        # Collecter le fichier via HTTP si nécessaire
        if not self._collect_csv_via_http(csv_file):
            print(f"Impossible de collecter {csv_file} via HTTP")
            return
        
        try:
            # Lire le fichier CSV
            df = pd.read_csv(csv_file)
            
            # Renommer les colonnes pour correspondre à notre schéma
            df.columns = ['Nom', 'ID_Reference', 'Prix', 'Stock']
            
            # Insérer les données
            cursor = self.db_manager.connection.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO PRODUIT 
                    (ID_Reference, Nom, Prix, Stock)
                    VALUES (?, ?, ?, ?)
                """, (row['ID_Reference'], row['Nom'], 
                     row['Prix'], row['Stock']))
            
            self.db_manager.connection.commit()
            print(f"{len(df)} produits importés avec succès")
            
        except Exception as e:
            print(f"Erreur lors de l'import des produits: {e}")
            self.db_manager.connection.rollback()
            raise
    
    def import_ventes(self, csv_file: str = "ventes.csv"):
        """
        Importe les données des ventes avec gestion des doublons
        
        Args:
            csv_file: Chemin vers le fichier CSV des ventes
        """
        print(f"Import des ventes depuis {csv_file}...")
        
        # Collecter le fichier via HTTP si nécessaire
        if not self._collect_csv_via_http(csv_file):
            print(f"Impossible de collecter {csv_file} via HTTP")
            return
        
        try:
            # Lire le fichier CSV
            df = pd.read_csv(csv_file)
            
            # Renommer les colonnes pour correspondre à notre schéma
            df.columns = ['Date', 'ID_Reference_Produit', 'Quantite', 'ID_Magasin']
            
            # Calculer le montant total pour chaque vente
            cursor = self.db_manager.connection.cursor()
            
            # Récupérer les prix des produits
            prix_produits = {}
            cursor.execute("SELECT ID_Reference, Prix FROM PRODUIT")
            for row in cursor.fetchall():
                prix_produits[row[0]] = row[1]
            
            # Préparer les données avec montant total
            ventes_to_insert = []
            nouvelles_ventes = 0
            
            for _, row in df.iterrows():
                # Calculer le montant total
                prix = prix_produits.get(row['ID_Reference_Produit'], 0)
                montant_total = row['Quantite'] * prix
                
                # Vérifier si cette vente existe déjà
                cursor.execute("""
                    SELECT COUNT(*) FROM VENTE 
                    WHERE Date = ? AND ID_Reference_Produit = ? 
                    AND Quantite = ? AND ID_Magasin = ?
                """, (row['Date'], row['ID_Reference_Produit'], 
                     row['Quantite'], row['ID_Magasin']))
                
                if cursor.fetchone()[0] == 0:  # Vente n'existe pas
                    ventes_to_insert.append((
                        row['Date'], row['ID_Reference_Produit'], 
                        row['Quantite'], row['ID_Magasin'], montant_total
                    ))
                    nouvelles_ventes += 1
            
            # Insérer les nouvelles ventes
            if ventes_to_insert:
                cursor.executemany("""
                    INSERT INTO VENTE 
                    (Date, ID_Reference_Produit, Quantite, ID_Magasin, Montant_Total)
                    VALUES (?, ?, ?, ?, ?)
                """, ventes_to_insert)
                
                self.db_manager.connection.commit()
                print(f"{nouvelles_ventes} nouvelles ventes importées")
            else:
                print("Aucune nouvelle vente à importer (toutes existent déjà)")
            
        except Exception as e:
            print(f"Erreur lors de l'import des ventes: {e}")
            self.db_manager.connection.rollback()
            raise
    
    def get_import_summary(self) -> dict:
        """
        Retourne un résumé des données importées
        
        Returns:
            dict: Résumé avec le nombre d'enregistrements par table
        """
        summary = {
            'magasins': self.db_manager.get_table_count('MAGASIN'),
            'produits': self.db_manager.get_table_count('PRODUIT'),
            'ventes': self.db_manager.get_table_count('VENTE'),
            'analyses': self.db_manager.get_table_count('ANALYSE_RESULTATS')
        }
        return summary

def main():
    """Fonction principale pour l'import des données"""
    print("Début de l'import des données...")
    
    # Initialiser le gestionnaire de base de données
    db_manager = DatabaseManager()
    
    try:
        # Se connecter à la base de données
        db_manager.connect()
        
        # Créer les tables si elles n'existent pas
        db_manager.create_tables()
        
        # Initialiser l'importeur
        importer = DataImporter(db_manager)
        
        # Importer les données dans l'ordre (magasins et produits d'abord)
        importer.import_magasins()
        importer.import_produits()
        importer.import_ventes()
        
        # Afficher le résumé
        summary = importer.get_import_summary()
        print("\nRésumé de l'import:")
        for table, count in summary.items():
            print(f"  - {table.capitalize()}: {count} enregistrements")
            
    except Exception as e:
        print(f"Erreur lors de l'import: {e}")
    finally:
        db_manager.close()

if __name__ == "__main__":
    main()
