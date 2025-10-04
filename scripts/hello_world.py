#!/usr/bin/env python3
"""
Script Hello World pour tester l'environnement Python
"""

def main():
    """Fonction principale du script Hello World"""
    print("Hello World - Test de l'environnement Python")
    print("=" * 50)
    
    # Test des imports de base
    try:
        import sys
        import os
        import sqlite3
        print("Imports de base réussis")
    except ImportError as e:
        print(f"Erreur d'import: {e}")
        return 1
    
    # Test de la version Python
        print(f"Version Python: {sys.version}")
    
    # Test de l'accès au système de fichiers
    try:
        current_dir = os.getcwd()
        print(f"Répertoire de travail: {current_dir}")
    except Exception as e:
        print(f"Erreur accès fichiers: {e}")
        return 1
    
    # Test de SQLite
    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        print(f"Test SQLite réussi: {result[0]}")
    except Exception as e:
        print(f"Erreur SQLite: {e}")
        return 1
    
    print("=" * 50)
    print("Hello World terminé avec succès!")
    print("L'environnement Python est prêt pour le projet")
    print("=" * 50)
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
