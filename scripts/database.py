#!/usr/bin/env python3

import sqlite3
import os
from typing import Optional

class DatabaseManager:
    
    def __init__(self, db_path: str = "data/ventes.db"):
        self.db_path = db_path
        self.connection: Optional[sqlite3.Connection] = None
        
    def connect(self) -> sqlite3.Connection:
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            print(f"Connexion à la base de données établie: {self.db_path}")
            return self.connection
        except Exception as e:
            print(f"Erreur de connexion à la base de données: {e}")
            raise
    
    def create_tables(self):
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS MAGASIN (
                    ID_Magasin INTEGER PRIMARY KEY,
                    Ville TEXT NOT NULL,
                    Nombre_Salaries INTEGER NOT NULL,
                    Region TEXT NOT NULL
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS PRODUIT (
                    ID_Reference TEXT PRIMARY KEY,
                    Nom TEXT NOT NULL,
                    Prix REAL NOT NULL CHECK (Prix > 0),
                    Stock INTEGER NOT NULL CHECK (Stock >= 0)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS VENTE (
                    ID_Vente INTEGER PRIMARY KEY AUTOINCREMENT,
                    Date TEXT NOT NULL,
                    ID_Reference_Produit TEXT NOT NULL,
                    Quantite INTEGER NOT NULL CHECK (Quantite > 0),
                    ID_Magasin INTEGER NOT NULL,
                    Montant_Total REAL NOT NULL,
                    FOREIGN KEY (ID_Reference_Produit) REFERENCES PRODUIT(ID_Reference),
                    FOREIGN KEY (ID_Magasin) REFERENCES MAGASIN(ID_Magasin)
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ANALYSE_RESULTATS (
                    ID_Analyse INTEGER PRIMARY KEY AUTOINCREMENT,
                    Type_Analyse TEXT NOT NULL,
                    Date_Analyse TEXT NOT NULL,
                    Resultat TEXT NOT NULL,
                    Valeur_Numerique REAL
                )
            """)
            
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_vente_date ON VENTE(Date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_vente_magasin ON VENTE(ID_Magasin)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_vente_produit ON VENTE(ID_Reference_Produit)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_analyse_type ON ANALYSE_RESULTATS(Type_Analyse)")
            
            self.connection.commit()
            print("Tables créées avec succès")
            
        except Exception as e:
            print(f"Erreur lors de la création des tables: {e}")
            self.connection.rollback()
            raise
    
    def get_region_from_city(self, city: str) -> str:
        regions = {
            'Paris': 'Île-de-France',
            'Marseille': 'Provence-Alpes-Côte d\'Azur',
            'Lyon': 'Auvergne-Rhône-Alpes',
            'Bordeaux': 'Nouvelle-Aquitaine',
            'Lille': 'Hauts-de-France',
            'Nantes': 'Pays de la Loire',
            'Strasbourg': 'Grand Est'
        }
        return regions.get(city, 'Région inconnue')
    
    def check_table_exists(self, table_name: str) -> bool:
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        
        return cursor.fetchone() is not None
    
    def get_table_count(self, table_name: str) -> int:
        if not self.connection:
            self.connect()
            
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]
    
    def close(self):
        if self.connection:
            self.connection.close()
            print("Connexion à la base de données fermée")

if __name__ == "__main__":
    print("Initialisation de la base de données...")
    
    db_manager = DatabaseManager()
    try:
        db_manager.connect()
        db_manager.create_tables()
        
        tables = ['MAGASIN', 'PRODUIT', 'VENTE', 'ANALYSE_RESULTATS']
        for table in tables:
            if db_manager.check_table_exists(table):
                count = db_manager.get_table_count(table)
                print(f"Table {table}: {count} enregistrements")
            else:
                print(f"Table {table} non trouvée")
                
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        db_manager.close()
