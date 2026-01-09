import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(
    page_title="🤖 Euromillions Bot Pro",
    layout="wide"
)

st.title("🤖 Euromillions Bot Pro")
st.write("Gère ton budget, génère des grilles intelligentes et simule des tirages Euromillions de manière responsable.")
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

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Dépense actuelle : {manager.depense:.2f} €")
        st.write(f"Budget restant : {manager.reste():.2f} €")
    with col2:
        progress = min(manager.depense / budget_val, 1.0)
        st.progress(progress)
        if progress >= 1:
            st.error("🚫 Budget mensuel atteint")

except Exception as e:
    st.error(f"Erreur BudgetManager : {e}")
    BudgetManager = None
    st.divider()
st.subheader("🎯 Grilles intelligentes avec historique")

try:
    from core.generator import generer_grille_intelligente
    from core.storage import sauvegarder_grille, charger_historique
    from core.budget import BudgetManager

    # réutilisation du manager
    if manager is None:
        budget_val = 20
        manager = BudgetManager(budget_val)

    nb_grilles = st.slider("Nombre de grilles à générer", min_value=1, max_value=10, value=3, step=1)

    if st.button("🧠 Générer grilles"):
        grilles = []
        for _ in range(nb_grilles):
            if manager.peut_jouer():
                manager.jouer()
                nums, stars = generer_grille_intelligente()
                grilles.append((nums, stars))
                sauvegarder_grille(nums, stars)
        if grilles:
            for i, (nums, stars) in enumerate(grilles, 1):
                st.success(f"Grille {i}: Numéros {nums} ⭐ Étoiles {stars}")
            st.info(f"Budget restant : {manager.reste():.2f} €")
        else:
            st.error("🚫 Budget dépassé — impossible de générer des grilles")

    # afficher l'historique complet
    historique = charger_historique()
    if historique:
        st.write("📜 **Historique complet des grilles jouées**")
        for i, g in enumerate(historique, 1):
            st.write(f"{i}: Numéros {g['numeros']} ⭐ Étoiles {g['etoiles']}")
    else:
        st.info("Aucune grille jouée pour l'instant.")

except Exception as e:
    st.error(f"Erreur génération intelligente avec historique : {e}")

# ROI simulé
cout_total = len(historique) * 2.5
gains_total = 0  # ici tu peux simuler ou ajouter de vrais gains
st.metric("💸 Dépense totale", f"{cout_total:.2f} €")
st.metric("📈 ROI simulé", f"{gains_total - cout_total:.2f} €")


# --- Statistiques des numéros ---
st.subheader("📊 Statistiques")
try:
    from stats.analysis import frequences_numeros

    freq = frequences_numeros() if 'frequences_numeros' in globals() else pd.Series(dtype=int)
    if freq is not None and not freq.empty:
        fig, ax = plt.subplots(figsize=(10,4))
        freq.plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Fréquence des numéros joués")
        ax.set_xlabel("Numéro")
        ax.set_ylabel("Occurrences")
        st.pyplot(fig)
    else:
        st.info("Pas encore assez de données pour afficher des stats.")
except Exception as e:
    st.error(f"Erreur statistiques : {e}")

st.divider()

# --- Simulation Monte Carlo ---
st.subheader("🧪 Simulation Monte Carlo")
try:
    from ai.simulation import simuler

    nb = st.slider("Nombre de grilles simulées pour la simulation", min_value=1000, max_value=100_000, step=1000, value=10_000)

    if st.button("🚀 Lancer simulation"):
        gains, cout = simuler(nb)
        col1, col2, col3 = st.columns(3)
        col1.metric("💸 Coût total", f"{cout:,.2f} €")
        col2.metric("🏆 Gains simulés", f"{gains:,.2f} €")
        col3.metric("📉 Résultat net", f"{gains - cout:,.2f} €")
        st.warning(
            "Cette simulation montre l'espérance négative du jeu.\n"
            "Même avec beaucoup de grilles, perdre est la norme."
        )

except Exception as e:
    st.error(f"Erreur simulation : {e}")

st.divider()
st.info("✅ App prête à être utilisée sur Streamlit Cloud, avec grilles multiples et budget respecté.")
