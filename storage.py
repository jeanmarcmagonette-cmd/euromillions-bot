import json
from datetime import datetime
from pathlib import Path

DATA_PATH = Path("data/history.json")

def sauvegarder_grille(numeros, etoiles, prix):
    DATA_PATH.parent.mkdir(exist_ok=True)

    if DATA_PATH.exists():
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append({
        "date": datetime.now().isoformat(),
        "numeros": numeros,
        "etoiles": etoiles,
        "prix": prix,
        "gain": 0
    })

    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)
