import json
from pathlib import Path
import pandas as pd

DATA_PATH = Path("data/history.json")


def charger_donnees():
    if not DATA_PATH.exists():
        return []
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def total_depense():
    return sum(d["prix"] for d in charger_donnees())


def total_gains():
    return sum(d.get("gain", 0) for d in charger_donnees())


def roi():
    dep = total_depense()
    if dep == 0:
        return 0
    return round((total_gains() - dep) / dep * 100, 2)


def dataframe_historique():
    data = charger_donnees()
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)


def frequences_numeros():
    df = dataframe_historique()
    if df.empty:
        return None

    nums = []
    for ligne in df["numeros"]:
        nums.extend(ligne)

    return pd.Series(nums).value_counts().sort_index()
