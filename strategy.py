import random

def generer_grille_intelligente():
    poids = {i: 1 for i in range(1, 51)}

    # pénaliser numéros "humains" (dates)
    for i in range(1, 32):
        poids[i] *= 0.7

    population = list(poids.keys())
    poids_vals = list(poids.values())

    numeros = set()
    while len(numeros) < 5:
        numeros.add(random.choices(population, poids_vals)[0])

    etoiles = sorted(random.sample(range(1, 13), 2))
    return sorted(numeros), etoiles
