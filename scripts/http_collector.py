#!/usr/bin/env python3
"""
Script de collecte HTTP des données CSV
"""

import requests
import os
from typing import Optional

class DataCollector:
    """Collecteur de données via HTTP"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialise le collecteur de données
        
        Args:
            base_url: URL de base pour les données
        """
        self.base_url = base_url
        
    def download_csv(self, filename: str, url: Optional[str] = None) -> bool:
        """
        Télécharge un fichier CSV via HTTP
        
        Args:
            filename: Nom du fichier à télécharger
            url: URL complète (optionnelle)
            
        Returns:
            bool: True si le téléchargement a réussi
        """
        if url is None:
            url = f"{self.base_url}/{filename}"
            
        print(f"Téléchargement de {filename} depuis {url}...")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Sauvegarder le fichier
            with open(filename, 'wb') as f:
                f.write(response.content)
                
            print(f"{filename} téléchargé avec succès ({len(response.content)} bytes)")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors du téléchargement de {filename}: {e}")
            return False
        except Exception as e:
            print(f"Erreur inattendue pour {filename}: {e}")
            return False
    
    def collect_all_data(self) -> bool:
        """
        Collecte tous les fichiers de données
        
        Returns:
            bool: True si tous les téléchargements ont réussi
        """
        print("Début de la collecte des données via HTTP")
        print("=" * 50)
        
        files_to_download = [
            "magasins.csv",
            "produits.csv", 
            "ventes.csv"
        ]
        
        success_count = 0
        
        for filename in files_to_download:
            if self.download_csv(filename):
                success_count += 1
        
        print("=" * 50)
        print(f"Collecte terminée: {success_count}/{len(files_to_download)} fichiers téléchargés")
        
        if success_count == len(files_to_download):
            print("Tous les fichiers ont été téléchargés avec succès")
            return True
        else:
            print("Certains fichiers n'ont pas pu être téléchargés")
            return False
    
    def create_local_server(self) -> bool:
        """
        Crée un serveur HTTP local pour servir les fichiers CSV
        (Simulation pour les tests)
        
        Returns:
            bool: True si le serveur a été créé
        """
        print("Création d'un serveur HTTP local pour les tests...")
        
        try:
            from http.server import HTTPServer, SimpleHTTPRequestHandler
            import threading
            import time
            
            # Vérifier que les fichiers CSV existent
            csv_files = ["magasins.csv", "produits.csv", "ventes.csv"]
            missing_files = []
            
            for file in csv_files:
                if not os.path.exists(file):
                    missing_files.append(file)
            
            if missing_files:
                print(f"Fichiers manquants: {missing_files}")
                return False
            
            # Créer le serveur HTTP
            server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
            
            def run_server():
                print("Serveur HTTP démarré sur http://localhost:8000")
                server.serve_forever()
            
            # Démarrer le serveur dans un thread
            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            
            # Attendre que le serveur démarre
            time.sleep(1)
            
            print("Serveur HTTP local créé avec succès")
            return True
            
        except Exception as e:
            print(f"Erreur lors de la création du serveur: {e}")
            return False

def main():
    """Fonction principale pour la collecte des données"""
    print("COLLECTE DES DONNEES VIA HTTP")
    print("=" * 60)
    
    collector = DataCollector()
    
    # Créer un serveur local pour les tests
    if collector.create_local_server():
        print("\nTest de la collecte HTTP...")
        
        # Tester la collecte (les fichiers seront téléchargés depuis le serveur local)
        success = collector.collect_all_data()
        
        if success:
            print("\nCollecte HTTP testée avec succès!")
            print("Note: En production, remplacer 'localhost:8000' par l'URL réelle du client")
        else:
            print("\nProblème lors de la collecte HTTP")
            return 1
    else:
        print("Impossible de créer le serveur de test")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
