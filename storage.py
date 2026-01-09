import json
import os

HISTORY_FILE = "data/history.json"

def sauvegarder_grille(numeros, etoiles):
    """Ajoute une grille au fichier history.json"""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    
    data = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []

    data.append({
        "numeros": numeros,
        "etoiles": etoiles
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def charger_historique():
    """Retourne la liste des grilles jouées"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []
