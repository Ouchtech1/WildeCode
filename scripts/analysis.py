#!/usr/bin/env python3

import sqlite3
import json
from datetime import datetime
from database import DatabaseManager

class SalesAnalyzer:
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        
    def get_chiffre_affaires_total(self):
        print("Calcul du chiffre d'affaires total...")
        
        cursor = self.db_manager.connection.cursor()
        
        cursor.execute("""
            SELECT 
                SUM(Montant_Total) as CA_Total,
                COUNT(*) as Nombre_Ventes,
                MIN(Date) as Date_Debut,
                MAX(Date) as Date_Fin
            FROM VENTE
        """)
        
        result = cursor.fetchone()
        
        analysis_result = {
            'type_analyse': 'CA_TOTAL',
            'date_analyse': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'chiffre_affaires_total': round(result[0], 2) if result[0] else 0,
            'nombre_ventes': result[1],
            'periode_debut': result[2],
            'periode_fin': result[3]
        }
        
        self._store_analysis_result(analysis_result)
        
        print(f"CA Total: {analysis_result['chiffre_affaires_total']}€")
        return analysis_result
    
    def get_ventes_par_produit(self):
        print("Analyse des ventes par produit...")
        
        cursor = self.db_manager.connection.cursor()
        
        cursor.execute("""
            SELECT 
                p.ID_Reference,
                p.Nom,
                p.Prix,
                SUM(v.Quantite) as Quantite_Totale,
                SUM(v.Montant_Total) as CA_Produit,
                COUNT(v.ID_Vente) as Nombre_Ventes
            FROM PRODUIT p
            LEFT JOIN VENTE v ON p.ID_Reference = v.ID_Reference_Produit
            GROUP BY p.ID_Reference, p.Nom, p.Prix
            ORDER BY CA_Produit DESC
        """)
        
        results = cursor.fetchall()
        
        produits_analysis = []
        for row in results:
            produits_analysis.append({
                'reference': row[0],
                'nom': row[1],
                'prix_unitaire': row[2],
                'quantite_totale': row[3] or 0,
                'ca_produit': round(row[4] or 0, 2),
                'nombre_ventes': row[5] or 0
            })
        
        analysis_result = {
            'type_analyse': 'VENTES_PRODUIT',
            'date_analyse': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'produits': produits_analysis,
            'nombre_produits': len(produits_analysis)
        }
        
        self._store_analysis_result(analysis_result)
        
        print(f"Analyse de {len(produits_analysis)} produits terminée")
        return analysis_result
    
    def get_ventes_par_region(self):
        print("Analyse des ventes par région...")
        
        cursor = self.db_manager.connection.cursor()
        
        cursor.execute("""
            SELECT 
                m.Region,
                COUNT(DISTINCT m.ID_Magasin) as Nombre_Magasins,
                SUM(v.Montant_Total) as CA_Region,
                COUNT(v.ID_Vente) as Nombre_Ventes,
                SUM(v.Quantite) as Quantite_Totale
            FROM MAGASIN m
            LEFT JOIN VENTE v ON m.ID_Magasin = v.ID_Magasin
            GROUP BY m.Region
            ORDER BY CA_Region DESC
        """)
        
        results = cursor.fetchall()
        
        regions_analysis = []
        for row in results:
            regions_analysis.append({
                'region': row[0],
                'nombre_magasins': row[1],
                'ca_region': round(row[2] or 0, 2),
                'nombre_ventes': row[3] or 0,
                'quantite_totale': row[4] or 0
            })
        
        analysis_result = {
            'type_analyse': 'VENTES_REGION',
            'date_analyse': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'regions': regions_analysis,
            'nombre_regions': len(regions_analysis)
        }
        
        self._store_analysis_result(analysis_result)
        
        print(f"Analyse de {len(regions_analysis)} régions terminée")
        return analysis_result
    
    def _store_analysis_result(self, result):
        cursor = self.db_manager.connection.cursor()
        
        valeur_numerique = None
        if 'chiffre_affaires_total' in result:
            valeur_numerique = result['chiffre_affaires_total']
        elif 'ca_total' in result:
            valeur_numerique = result['ca_total']
        
        cursor.execute("""
            INSERT INTO ANALYSE_RESULTATS 
            (Type_Analyse, Date_Analyse, Resultat, Valeur_Numerique)
            VALUES (?, ?, ?, ?)
        """, (
            result['type_analyse'],
            result['date_analyse'],
            json.dumps(result, ensure_ascii=False),
            valeur_numerique
        ))
        
        self.db_manager.connection.commit()
    
    def generate_summary_report(self):
        print("Génération du rapport de synthèse...")
        
        ca_total = self.get_chiffre_affaires_total()
        ventes_produits = self.get_ventes_par_produit()
        ventes_regions = self.get_ventes_par_region()
        
        produit_top = max(ventes_produits['produits'], key=lambda x: x['ca_produit'])
        region_top = max(ventes_regions['regions'], key=lambda x: x['ca_region'])
        
        summary = {
            'date_generation': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'chiffre_affaires_total': ca_total['chiffre_affaires_total'],
            'nombre_ventes_total': ca_total['nombre_ventes'],
            'produit_top': {
                'nom': produit_top['nom'],
                'reference': produit_top['reference'],
                'ca': produit_top['ca_produit']
            },
            'region_top': {
                'nom': region_top['region'],
                'ca': region_top['ca_region'],
                'magasins': region_top['nombre_magasins']
            },
            'periode_analyse': {
                'debut': ca_total['periode_debut'],
                'fin': ca_total['periode_fin']
            }
        }
        
        print("Rapport de synthèse généré")
        return summary

if __name__ == "__main__":
    print("Début de l'analyse des ventes...")
    
    db_manager = DatabaseManager()
    
    try:
        db_manager.connect()
        
        analyzer = SalesAnalyzer(db_manager)
        summary = analyzer.generate_summary_report()
        
        print("\n" + "="*50)
        print("RAPPORT D'ANALYSE DES VENTES")
        print("="*50)
        print(f"Chiffre d'affaires total: {summary['chiffre_affaires_total']}€")
        print(f"Nombre total de ventes: {summary['nombre_ventes_total']}")
        print(f"Produit le plus vendu: {summary['produit_top']['nom']} ({summary['produit_top']['ca']}€)")
        print(f"Région la plus performante: {summary['region_top']['nom']} ({summary['region_top']['ca']}€)")
        print(f"Période analysée: {summary['periode_analyse']['debut']} à {summary['periode_analyse']['fin']}")
        print("="*50)
        
    except Exception as e:
        print(f"Erreur lors de l'analyse: {e}")
    finally:
        db_manager.close()
