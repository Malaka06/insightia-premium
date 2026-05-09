import streamlit as st
from ui.theme import apply_theme

PAGES = ["Accueil", "Démarrer", "Executive View", "Analysis Explorer", "Prioritization Board", "Reports"]

def setup_page():
    st.set_page_config(page_title="InsightIA", page_icon="🧠", layout="wide")
    apply_theme()


def top_nav():
    if "page" not in st.session_state:
        st.session_state.page = "Accueil"
    cols = st.columns([1.2, 1, 1, 1, 1, 1])
    labels = PAGES
    for col, label in zip(cols, labels):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.page = label
                st.rerun()
