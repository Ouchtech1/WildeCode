#!/bin/bash

# Script de test de la collecte HTTP intégrée
echo "=========================================="
echo "TEST DE LA COLLECTE HTTP INTEGREE"
echo "=========================================="

# 1. Démarrer le serveur HTTP en arrière-plan
echo ""
echo "1. Démarrage du serveur HTTP sur le port 8000..."
python3 -m http.server 8000 > /dev/null 2>&1 &
SERVER_PID=$!
echo "   Serveur démarré (PID: $SERVER_PID)"

# Attendre que le serveur démarre
sleep 2

# 2. Vérifier que le serveur répond
echo ""
echo "2. Vérification du serveur..."
if curl -s http://localhost:8000/magasins.csv > /dev/null; then
    echo "   Serveur HTTP opérationnel"
else
    echo "   ERREUR: Serveur HTTP non accessible"
    kill $SERVER_PID
    exit 1
fi

# 3. Supprimer les fichiers CSV locaux pour forcer le téléchargement
echo ""
echo "3. Suppression des CSV locaux (pour forcer le téléchargement)..."
rm -f magasins.csv produits.csv ventes.csv
echo "   Fichiers supprimés"

# 4. Exécuter le script principal avec collecte HTTP
echo ""
echo "4. Lancement du script principal avec USE_HTTP=true..."
echo "=========================================="
source venv/bin/activate
USE_HTTP=true HTTP_BASE_URL=http://localhost:8000 python scripts/main.py
EXIT_CODE=$?

# 5. Arrêter le serveur
echo ""
echo "=========================================="
echo "5. Arrêt du serveur HTTP..."
kill $SERVER_PID
echo "   Serveur arrêté"

# 6. Résultat du test
echo ""
echo "=========================================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "TEST REUSSI - Collecte HTTP fonctionnelle"
else
    echo "TEST ECHOUE - Code de sortie: $EXIT_CODE"
fi
echo "=========================================="

exit $EXIT_CODE

