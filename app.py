import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import os
import json

st.set_page_config(page_title="🤖 Euromillions Bot Pro", layout="wide")
st.title("🤖 Euromillions Bot Pro – Version Ultra Pro")
st.write("Gère ton budget, génère des grilles intelligentes et simule des tirages Euromillions avec style !")
st.divider()

# -----------------------------
# Initialisation BudgetManager
# -----------------------------
from core.budget import BudgetManager

budget_val = st.sidebar.number_input("Budget mensuel (€)", min_value=5, max_value=200, value=20)

if "manager" not in st.session_state:
    st.session_state.manager = BudgetManager(budget_val)
manager = st.session_state.manager

# -----------------------------
# Bouton Réinitialiser
# -----------------------------
history_file = "data/history.json"
if st.sidebar.button("🔄 Réinitialiser tout"):
    if "manager" in st.session_state:
        del st.session_state.manager
    if os.path.exists(history_file):
        with open(history_file, "w") as f:
            json.dump([], f)
    st.sidebar.success("✅ Budget et historique remis à zéro. Rechargez la page.")

# -----------------------------
# Layout 3 colonnes
# -----------------------------
col_budget, col_grilles, col_simulation = st.columns([1,2,2])

# -----------------------------
# Colonne 1 : Budget stylé avec live update
# -----------------------------
with col_budget:
    st.subheader("💰 Budget")
    budget_placeholder = st.empty()  # placeholder pour le budget live

# Fonction pour mettre à jour le budget dans la colonne 1
def afficher_budget():
    depense = manager.depense
    restant = manager.reste()
    progress = min(depense / manager.budget, 1.0)

    # Couleur dynamique
    if progress < 0.5:
        color = "green"
    elif progress < 0.8:
        color = "orange"
    else:
        color = "red"

    with budget_placeholder.container():
        st.markdown(f"<h3>Dépense actuelle : {depense:.2f} €</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3>Budget restant : {restant:.2f} €</h3>", unsafe_allow_html=True)
        st.progress(progress)
        if progress >= 1:
            st.error("🚫 Budget mensuel atteint")

# Affichage initial
afficher_budget()

# -----------------------------
# Colonne 2 : Grilles + Historique
# -----------------------------
with col_grilles:
    st.subheader("🎯 Générateur de grilles")
    from core.generator import generer_grille_intelligente
    from core.storage import sauvegarder_grille, charger_historique

    nb_grilles = st.slider("Nombre de grilles", 1, 10, 3, key="slider_nb_grilles")

    if st.button("🧠 Générer grilles", key="btn_generer_grilles"):
        grilles = []
        for _ in range(nb_grilles):
            if manager.peut_jouer():
                manager.jouer()  # ✅ dépense mise à jour
                nums, stars = generer_grille_intelligente()
                grilles.append((nums, stars))
                sauvegarder_grille(nums, stars)

        # Mettre à jour le budget live
        afficher_budget()

        # Affichage des grilles générées
        if grilles:
            for i, (nums, stars) in enumerate(grilles, 1):
                st.success(f"Grille {i}: Numéros {nums} ⭐ Étoiles {stars}")
        else:
            st.error("🚫 Budget dépassé — impossible de générer des grilles")

    # Historique stylé
    historique = charger_historique()
    if historique:
        st.subheader("📜 Historique des grilles")
        for g in historique[-10:][::-1]:
            st.info(f"Numéros {g['numeros']} ⭐ Étoiles {g['etoiles']}")
        cout_total = len(historique)*2.5
        gains_total = 0
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💸 Dépense totale", f"{cout_total:.2f} €")
        with col2:
            st.metric("📈 ROI simulé", f"{gains_total - cout_total:.2f} €",
                      delta_color="inverse" if gains_total - cout_total < 0 else "normal")
    else:
        st.info("Aucune grille jouée pour l'instant.")

# -----------------------------
# Colonne 3 : Simulation Monte Carlo + Stats
# -----------------------------
with col_simulation:
    st.subheader("🧪 Simulation Monte Carlo")
    from ai.simulation import simuler
    from stats.analysis import frequences_numeros

    nb_sim = st.slider("Grilles simulées", 1000, 100_000, 10_000, step=1000)
    if st.button("🚀 Lancer simulation", key="btn_simuler"):
        gains, cout = simuler(nb_sim)
        col1, col2, col3 = st.columns(3)
        col1.metric("💸 Coût total", f"{cout:,.2f} €")
        col2.metric("🏆 Gains simulés", f"{gains:,.2f} €")
        col3.metric("📉 Résultat net", f"{gains - cout:.2f} €",
                    delta_color="inverse" if gains - cout < 0 else "normal")
        st.warning("Simulation Monte Carlo — l'espérance est négative.")

    # Statistiques des numéros
    freq = frequences_numeros()
    if freq is not None and not freq.empty:
        fig, ax = plt.subplots(figsize=(8,3))
        freq.plot(kind="bar", ax=ax, color="lightblue")
        ax.set_title("Fréquence des numéros joués")
        ax.set_xlabel("Numéro")
        ax.set_ylabel("Occurrences")
        st.pyplot(fig)
    else:
        st.info("Pas assez de données pour afficher des stats.")
