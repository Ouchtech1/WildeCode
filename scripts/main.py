#!/usr/bin/env python3

import sys
import os
from database import DatabaseManager
from import_data import DataImporter
from analysis import SalesAnalyzer

def main():
    print("DEMARRAGE DU PROJET D'ANALYSE DES VENTES PME")
    print("=" * 60)
    
    db_manager = DatabaseManager()
    
    try:
        print("\nETAPE 1: Initialisation de la base de données")
        print("-" * 40)
        db_manager.connect()
        db_manager.create_tables()
        
        print("\nETAPE 2: Import des données CSV")
        print("-" * 40)
        
        use_http = os.getenv('USE_HTTP', 'false').lower() == 'true'
        http_url = os.getenv('HTTP_BASE_URL', 'http://localhost:8000')
        
        if use_http:
            print(f"Mode collecte HTTP activé: {http_url}")
        
        importer = DataImporter(db_manager, use_http=use_http, base_url=http_url)
        
        importer.import_magasins()
        importer.import_produits()
        importer.import_ventes()
        
        summary = importer.get_import_summary()
        print(f"\nImport terminé:")
        for table, count in summary.items():
            print(f"   - {table.capitalize()}: {count} enregistrements")
        
        print("\nETAPE 3: Exécution des analyses")
        print("-" * 40)
        analyzer = SalesAnalyzer(db_manager)
        
        summary_report = analyzer.generate_summary_report()
        
        print("\nETAPE 4: Résultats détaillés")
        print("-" * 40)
        
        print(f"\nCHIFFRE D'AFFAIRES TOTAL")
        print(f"   Montant: {summary_report['chiffre_affaires_total']}€")
        print(f"   Nombre de ventes: {summary_report['nombre_ventes_total']}")
        
        print(f"\nPRODUIT LE PLUS VENDU")
        print(f"   Nom: {summary_report['produit_top']['nom']}")
        print(f"   Référence: {summary_report['produit_top']['reference']}")
        print(f"   CA généré: {summary_report['produit_top']['ca']}€")
        
        print(f"\nREGION LA PLUS PERFORMANTE")
        print(f"   Région: {summary_report['region_top']['nom']}")
        print(f"   CA généré: {summary_report['region_top']['ca']}€")
        print(f"   Nombre de magasins: {summary_report['region_top']['magasins']}")
        
        print(f"\nPERIODE D'ANALYSE")
        print(f"   Du: {summary_report['periode_analyse']['debut']}")
        print(f"   Au: {summary_report['periode_analyse']['fin']}")
        
        print("\n" + "=" * 60)
        print("PROJET TERMINE AVEC SUCCES!")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"\nERREUR CRITIQUE: {e}")
        print("=" * 60)
        return 1
        
    finally:
        db_manager.close()

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
