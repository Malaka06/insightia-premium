import streamlit as st
from ui.components.cards import glass_card


def render():
    st.markdown("""
    <div class='hero-card'>
        <span class='badge'>Voice of Customer Decision Intelligence</span>
        <div class='hero-title'>Transformez des milliers de retours clients en décisions prioritaires.</div>
        <p class='hero-subtitle'>InsightIA détecte les irritants critiques, les frustrations récurrentes et les signaux faibles afin d’aider les équipes produit, CX et direction à prioriser les bonnes actions.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Tester une démo", use_container_width=True, type="primary"):
            st.session_state.page = "Démarrer"
            st.rerun()
    with c2:
        if st.button("Importer mes données", use_container_width=True):
            st.session_state.page = "Démarrer"
            st.rerun()

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        glass_card("Taxonomie explicable", "Chaque classification est justifiée par des mots clés et une logique métier contrôlée.", "Explainable")
    with col2:
        glass_card("Priorisation business", "Les verbatims sont transformés en backlog actionnable avec criticité, fréquence et impact.", "Decision Layer")
    with col3:
        glass_card("3 univers de démo", "E-commerce, SaaS B2B et services consulaires pour démontrer l’adaptabilité du produit.", "Portfolio Senior")
