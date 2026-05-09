import streamlit as st

from core.loader import read_csv_robust, load_demo, standardize_columns
from core.nlp import run_pipeline
from core.prioritization import build_backlog


DEMOS = {
    "ecommerce": {
        "title": "RetailCX Intelligence",
        "subtitle": "E-commerce, livraison, SAV et remboursement",
        "story": "La majorité des frustrations clients ne provient pas des produits mais de l’expérience post-achat.",
    },
    "saas": {
        "title": "SaaS Product Signals",
        "subtitle": "Onboarding, activation, bugs et support produit",
        "story": "Le churn utilisateur commence souvent avant même l’activation complète du produit.",
    },
    "embassy": {
        "title": "Consular Experience Intelligence",
        "subtitle": "Ambassade du Congo, demandes consulaires et expérience citoyenne",
        "story": "Les frustrations administratives détruisent la confiance citoyenne avant même la qualité du service rendu.",
    },
}


def process_dataset(df, source_name: str):
    df = standardize_columns(df)
    analysis_df = run_pipeline(df)
    backlog_df = build_backlog(analysis_df)

    st.session_state.dataset = df
    st.session_state.analysis_df = analysis_df
    st.session_state.backlog_df = backlog_df
    st.session_state.selected_demo = source_name


def render_start(on_success=None):
    st.markdown("## Choisissez votre point de départ")
    st.caption("Testez une démo métier ou importez vos propres données pour générer une analyse personnalisée.")

    st.markdown("### Tester une démo")

    cols = st.columns(3)

    for col, (demo_key, demo) in zip(cols, DEMOS.items()):
        with col:
            st.markdown(
                f"""
                <div class="premium-card">
                    <h3>{demo["title"]}</h3>
                    <p class="muted">{demo["subtitle"]}</p>
                    <p><strong>{demo["story"]}</strong></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(f"Lancer {demo['title']}", key=f"demo_{demo_key}", use_container_width=True):
                try:
                    df = load_demo(demo_key)
                    process_dataset(df, demo["title"])
                    st.success(f"Démo chargée : {demo['title']}")

                    if on_success:
                        on_success()

                except Exception as e:
                    st.error(f"Impossible de charger la démo : {e}")

    st.markdown("---")

    st.markdown("### Importer mes données")
    st.caption(
        "Importez un CSV contenant au minimum une colonne commentaire, feedback, message, avis ou verbatim."
    )

    uploaded_file = st.file_uploader(
        "Déposer un fichier CSV",
        type=["csv"],
        label_visibility="visible",
    )

    if uploaded_file is not None:
        try:
            raw_df = read_csv_robust(uploaded_file)
            preview_df = standardize_columns(raw_df)

            st.success("Fichier chargé avec succès.")

            c1, c2, c3 = st.columns(3)
            c1.metric("Lignes", len(preview_df))
            c2.metric("Colonnes", len(preview_df.columns))
            c3.metric("Canaux", preview_df["channel"].nunique())

            st.markdown("#### Aperçu des données détectées")
            st.dataframe(preview_df.head(20), use_container_width=True)

            if st.button("Lancer l’analyse", use_container_width=True):
                process_dataset(raw_df, "Import CSV")
                st.success("Analyse générée avec succès.")

                if on_success:
                    on_success()

        except Exception as e:
            st.error(f"Impossible de traiter le fichier : {e}")