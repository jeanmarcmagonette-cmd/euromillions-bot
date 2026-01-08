import random

def generer_grille():
    numeros = sorted(random.sample(range(1, 51), 5))
    etoiles = sorted(random.sample(range(1, 13), 2))
    return numeros, etoiles
