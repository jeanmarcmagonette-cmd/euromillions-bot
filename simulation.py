import random

PRIX_GRILLE = 2.5

def simuler(nb_grilles: int):
    cout_total = nb_grilles * PRIX_GRILLE
    gains_total = 0.0

    for _ in range(nb_grilles):
        r = random.random()

        if r < 0.000001:
            gains_total += 1_000_000
        elif r < 0.0001:
            gains_total += 1_000
        elif r < 0.01:
            gains_total += 20
        elif r < 0.1:
            gains_total += 5

    return gains_total, cout_total
