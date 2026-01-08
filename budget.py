class BudgetManager:
    def __init__(self, budget, prix_grille=2.5):
        self.budget = budget
        self.prix = prix_grille
        self.depense = 0.0

    def peut_jouer(self):
        return self.depense + self.prix <= self.budget

    def jouer(self):
        if self.peut_jouer():
            self.depense += self.prix
            return True
        return False

    def reste(self):
        return round(self.budget - self.depense, 2)
