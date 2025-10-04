#!/usr/bin/env python3
"""
Test de la collecte HTTP intégrée
"""

import os
import sys
from database import DatabaseManager
from import_data import DataImporter

def main():
    """Test de la collecte HTTP"""
    print("🧪 TEST DE LA COLLECTE HTTP INTÉGRÉE")
    print("=" * 50)
    
    # Créer un serveur HTTP simple
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    import threading
    import time
    
    print("🌐 Démarrage du serveur HTTP de test...")
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    
    def run_server():
        print("✅ Serveur HTTP démarré sur http://localhost:8000")
        server.serve_forever()
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(1)
    
    # Test de la collecte HTTP
    print("\n📋 Test de la collecte HTTP...")
    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.create_tables()
    
    # Utiliser la collecte HTTP
    importer = DataImporter(db_manager, use_http=True, base_url="http://localhost:8000")
    
    # Test d'import avec HTTP
    print("\n🔍 Test import magasins via HTTP...")
    importer.import_magasins()
    
    print("\n✅ Test de collecte HTTP terminé!")
    print("📝 En production, remplacer l'URL par celle du client")
    
    db_manager.close()
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
