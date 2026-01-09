import streamlit as st

from core.budget import BudgetManager
from core.generator import generer_grille_intelligente

st.set_page_config(page_title="Euromillions Bot", layout="centered")

st.title("🎯 Euromillions Bot")

# =========================
# INITIALISATION SESSION
# =========================
if "manager" not in st.session_state:
    st.session_state.manager = BudgetManager(budget=20)

# =========================
# AFFICHAGE BUDGET
# =========================
st.subheader("💰 Budget")

m = st.session_state.manager

st.metric("Dépense actuelle", f"{m.depense:.2f} €")
st.metric("Budget restant", f"{m.reste():.2f} €")
st.progress(min(m.depense / m.budget, 1.0))

st.divider()

# =========================
# GÉNÉRATION DE GRILLE
# =========================
st.subheader("🎲 Générer une grille")

if st.button("Générer une grille"):
    if m.jouer():
        nums, stars = generer_grille_intelligente()
        st.success(f"Grille générée : {nums} ⭐ {stars}")
    else:
        st.error("🚫 Budget dépassé")

# =========================
# DEBUG (IMPORTANT)
# =========================
st.caption(f"DEBUG — dépense = {m.depense}")
