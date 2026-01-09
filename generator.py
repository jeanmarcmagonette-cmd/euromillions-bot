import random

def generer_grille_intelligente():
    """
    Génère une grille Euromillions équilibrée :
    - répartition bas / moyen / haut
    - évite les suites évidentes
    """
    bas = random.sample(range(1, 17), 2)
    moyen = random.sample(range(17, 34), 2)
    haut = random.sample(range(34, 51), 1)

    numeros = sorted(bas + moyen + haut)

    # étoiles non consécutives
    e1 = random.randint(1, 12)
    e2 = random.randint(1, 12)
    while abs(e1 - e2) <= 1:
        e2 = random.randint(1, 12)

    etoiles = sorted([e1, e2])

    return numeros, etoiles
