import random

PRIX_GRILLE = 2.5
PROBA_JACKPOT = 1 / 139_838_160
GAIN_JACKPOT = 20_000_000

def simuler(nb_grilles):
    gains = 0
    for _ in range(nb_grilles):
        if random.random() < PROBA_JACKPOT:
            gains += GAIN_JACKPOT

    cout = nb_grilles * PRIX_GRILLE
    return gains, cout
