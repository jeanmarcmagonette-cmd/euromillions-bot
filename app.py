import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="🤖 Euromillions Bot",
    layout="centered"
)

st.title("🤖 Euromillions Bot Ultra-Pro")
st.write("Gère ton budget, analyse les numéros et simule des tirages Euromillions de manière responsable.")
st.divider()

# --- Gestion du budget ---
st.subheader("💰 Budget")
try:
    from core.budget import BudgetManager

    budget_val = st.number_input(
        "Budget mensuel (€)",
        min_value=5,
        max_value=200,
        value=20,
        key="budget_input"
    )
    manager = BudgetManager(budget_val)

    st.write(f"Dépenses actuelles : {manager.depense:.2f} €")
    st.write(f"Budget restant : {manager.reste():.2f} €")

    progress = min(manager.depense / budget_val, 1.0)
    st.progress(progress)
    if progress >= 1:
        st.error("🚫 Budget mensuel atteint")
except Exception as e:
    st.error(f"Erreur BudgetManager : {e}")
    BudgetManager = None

st.divider()

# --- Statistiques des numéros ---
st.subheader("📊 Statistiques")
try:
    from stats.analysis import frequences_numeros

    freq = frequences_numeros() if 'frequences_numeros' in globals() else pd.Series(dtype=int)
    if freq is not None and not freq.empty:
        fig, ax = plt.subplots()
        freq.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Fréquence des numéros joués")
        ax.set_xlabel("Numéro")
        ax.set_ylabel("Occurrences")
        st.pyplot(fig)
    else:
        st.info("Pas encore assez de données pour afficher des stats.")
except Exception as e:
    st.error(f"Erreur dans les statistiques : {e}")

st.divider()

# --- Simulation Monte Carlo ---
st.subheader("🧪 Simulation Monte Carlo")
try:
    from ai.simulation import simuler

    nb = st.slider("Nombre de grilles simulées", min_value=1000, max_value=100_000, step=1000, value=10_000)
    if st.button("🚀 Lancer la simulation"):
        gains, cout = simuler(nb)
        st.write(f"💸 Coût total : {cout:,.2f} €")
        st.write(f"🏆 Gains simulés : {gains:,.2f} €")
        st.write(f"📉 Résultat net : {gains - cout:,.2f} €")
        st.warning(
            "Cette simulation montre l'espérance négative du jeu.\n"
            "Même avec beaucoup de grilles, perdre est la norme."
        )
except Exception as e:
    st.error(f"Erreur dans la simulation : {e}")

st.divider()

# --- Générateur de grilles intelligente ---
st.subheader("🎯 Grille intelligente (avec budget)")

try:
    from core.generator import generer_grille_intelligente
    from core.budget import BudgetManager

    # on réutilise manager existant
    if manager is None:
        budget_val = 20
        manager = BudgetManager(budget_val)

    st.write(f"💸 Dépense actuelle : {manager.depense:.2f} €")
    st.write(f"💰 Budget restant : {manager.reste():.2f} €")

    if st.button("🧠 Générer une grille intelligente"):
        if manager.peut_jouer():
            manager.jouer()
            nums, stars = generer_grille_intelligente()
            st.success(f"🎟️ Numéros : {nums} ⭐ Étoiles : {stars}")
            st.info(f"Budget restant : {manager.reste():.2f} €")
        else:
            st.error("🚫 Budget dépassé — génération bloquée")

except Exception as e:
    st.error(f"Erreur génération intelligente : {e}")

st.divider()
st.info("✅ L'app est prête à être déployée sur Streamlit Cloud et ne devrait jamais afficher une page blanche.")

