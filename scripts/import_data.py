#!/usr/bin/env python3

import pandas as pd
import sqlite3
import requests
from database import DatabaseManager

class DataImporter:
    
    def __init__(self, db_manager: DatabaseManager, use_http: bool = False, base_url: str = "http://localhost:8000"):
        self.db_manager = db_manager
        self.use_http = use_http
        self.base_url = base_url
        
    def _collect_csv_via_http(self, filename: str) -> bool:
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
        print(f"Import des magasins depuis {csv_file}...")
        
        if not self._collect_csv_via_http(csv_file):
            print(f"Impossible de collecter {csv_file} via HTTP")
            return
        
        try:
            df = pd.read_csv(csv_file)
            df.columns = ['ID_Magasin', 'Ville', 'Nombre_Salaries']
            df['Region'] = df['Ville'].apply(self.db_manager.get_region_from_city)
            
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
        print(f"Import des produits depuis {csv_file}...")
        
        if not self._collect_csv_via_http(csv_file):
            print(f"Impossible de collecter {csv_file} via HTTP")
            return
        
        try:
            df = pd.read_csv(csv_file)
            df.columns = ['Nom', 'ID_Reference', 'Prix', 'Stock']
            
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
        print(f"Import des ventes depuis {csv_file}...")
        
        if not self._collect_csv_via_http(csv_file):
            print(f"Impossible de collecter {csv_file} via HTTP")
            return
        
        try:
            df = pd.read_csv(csv_file)
            df.columns = ['Date', 'ID_Reference_Produit', 'Quantite', 'ID_Magasin']
            
            cursor = self.db_manager.connection.cursor()
            
            prix_produits = {}
            cursor.execute("SELECT ID_Reference, Prix FROM PRODUIT")
            for row in cursor.fetchall():
                prix_produits[row[0]] = row[1]
            
            ventes_to_insert = []
            nouvelles_ventes = 0
            
            for _, row in df.iterrows():
                prix = prix_produits.get(row['ID_Reference_Produit'], 0)
                montant_total = row['Quantite'] * prix
                
                cursor.execute("""
                    SELECT COUNT(*) FROM VENTE 
                    WHERE Date = ? AND ID_Reference_Produit = ? 
                    AND Quantite = ? AND ID_Magasin = ?
                """, (row['Date'], row['ID_Reference_Produit'], 
                     row['Quantite'], row['ID_Magasin']))
                
                if cursor.fetchone()[0] == 0:
                    ventes_to_insert.append((
                        row['Date'], row['ID_Reference_Produit'], 
                        row['Quantite'], row['ID_Magasin'], montant_total
                    ))
                    nouvelles_ventes += 1
            
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
        summary = {
            'magasins': self.db_manager.get_table_count('MAGASIN'),
            'produits': self.db_manager.get_table_count('PRODUIT'),
            'ventes': self.db_manager.get_table_count('VENTE'),
            'analyses': self.db_manager.get_table_count('ANALYSE_RESULTATS')
        }
        return summary

if __name__ == "__main__":
    print("Début de l'import des données...")
    
    db_manager = DatabaseManager()
    
    try:
        db_manager.connect()
        db_manager.create_tables()
        
        importer = DataImporter(db_manager)
        
        importer.import_magasins()
        importer.import_produits()
        importer.import_ventes()
        
        summary = importer.get_import_summary()
        print("\nRésumé de l'import:")
        for table, count in summary.items():
            print(f"  - {table.capitalize()}: {count} enregistrements")
            
    except Exception as e:
        print(f"Erreur lors de l'import: {e}")
    finally:
        db_manager.close()
