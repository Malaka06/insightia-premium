import streamlit as st

from core.loader import load_demo, read_csv_robust, standardize_columns
from core.nlp import run_pipeline
from core.prioritization import build_backlog

from ui.theme import apply_theme
from ui.pages.executive import render_executive
from ui.pages.explorer import render_explorer
from ui.pages.backlog import render_backlog
from ui.pages.reports import render_reports


st.set_page_config(
    page_title="InsightIA — Analyse des retours clients",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()


def html(content: str):
    st.markdown(content, unsafe_allow_html=True)


DEMOS = {
    "ecommerce": {
        "title": "Expérience E-commerce",
        "label": "Retail · Livraison · SAV",
        "subtitle": "Analysez les irritants liés à la livraison, au remboursement et au support client.",
        "story": "Comprendre pourquoi certains clients perdent confiance après l’achat.",
        "button": "Analyser la démo E-commerce",
    },
    "saas": {
        "title": "Expérience SaaS",
        "label": "Produit · Adoption · Support",
        "subtitle": "Détectez les frictions qui ralentissent l’activation et la rétention.",
        "story": "Identifier les signaux qui empêchent les utilisateurs d’atteindre la valeur produit.",
        "button": "Analyser la démo SaaS",
    },
    "embassy": {
        "title": "Services Consulaires",
        "label": "Administration · Citoyens · Confiance",
        "subtitle": "Analysez les retours liés aux démarches administratives et consulaires.",
        "story": "Réduire les frictions administratives et améliorer la qualité du service.",
        "button": "Analyser la démo Consulaire",
    },
}


PAGES = [
    "Accueil",
    "Synthèse",
    "Frictions détectées",
    "Priorisation",
    "Rapports",
]


def init_state():
    st.session_state.setdefault("page", "Accueil")
    st.session_state.setdefault("analysis_df", None)
    st.session_state.setdefault("backlog_df", None)
    st.session_state.setdefault("current_demo", None)


def go_to(page: str):
    st.session_state.page = page
    st.rerun()


def load_analysis(df, demo_name=None):
    df = standardize_columns(df)
    analysis_df = run_pipeline(df)
    backlog_df = build_backlog(analysis_df)

    st.session_state.analysis_df = analysis_df
    st.session_state.backlog_df = backlog_df
    st.session_state.current_demo = demo_name
    st.session_state.page = "Synthèse"

    st.rerun()


def render_header():
    html("""
<section class="hero-wrapper">
<div class="hero-left">
<div class="hero-badge">INSIGHTIA · ANALYSE DES RETOURS CLIENTS</div>
<div class="hero-title">Transformez les retours clients en priorités d’action.</div>
<div class="hero-subtitle">InsightIA aide à repérer les sujets récurrents, les irritants les plus sensibles et les actions à prioriser à partir de verbatims clients.</div>
<div class="hero-proof">Analyse structurée · Priorisation métier · Recommandations opérationnelles</div>
</div>

<div class="hero-panel">
<div class="panel-label">Point d’attention</div>
<div class="panel-value">Prioritaire</div>
<div class="panel-title">Sujet client nécessitant une action rapide</div>
<div class="panel-text">Les sujets liés à la communication, au suivi ou aux délais peuvent rapidement dégrader la confiance client.</div>
<div class="panel-divider"></div>
<div class="panel-row"><span>Impact attendu</span><strong>Fort</strong></div>
<div class="panel-row"><span>Horizon conseillé</span><strong>30 jours</strong></div>
<div class="panel-row"><span>Équipes concernées</span><strong>CX · Produit · Opérations</strong></div>
</div>
</section>
""")


def render_navigation():
    cols = st.columns(len(PAGES))

    for col, page in zip(cols, PAGES):
        active = st.session_state.page == page
        label = f"● {page}" if active else page

        with col:
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                go_to(page)


def render_monitoring_preview():
    html("""
<div class="section-header compact">
<div class="section-kicker">LECTURE RAPIDE</div>
<div class="section-title">Ce que la plateforme aide à repérer</div>
<div class="section-description">InsightIA ne se limite pas à compter des commentaires : la plateforme aide à comprendre quels sujets reviennent, qui est concerné et quelles actions peuvent être utiles.</div>
</div>

<div class="insight-grid">
<div class="insight-card">
<div class="insight-badge risk">À TRAITER</div>
<div class="insight-title">Frictions récurrentes</div>
<div class="insight-text">Identifier les sujets qui reviennent régulièrement dans les retours clients et qui méritent une action concrète.</div>
</div>

<div class="insight-card">
<div class="insight-badge signal">À SURVEILLER</div>
<div class="insight-title">Signaux faibles</div>
<div class="insight-text">Repérer les problèmes encore peu volumineux mais susceptibles de prendre de l’importance.</div>
</div>

<div class="insight-card">
<div class="insight-badge action">À PRIORISER</div>
<div class="insight-title">Actions recommandées</div>
<div class="insight-text">Relier les irritants détectés à des actions simples, lisibles et orientées métier.</div>
</div>
</div>
""")


def render_home():
    html("""
<div class="section-header">
<div class="section-kicker">POINT DE DÉPART</div>
<div class="section-title">Choisissez votre environnement d’analyse</div>
<div class="section-description">Lancez une démonstration métier ou importez vos propres données pour obtenir une lecture structurée des irritants, des sujets récurrents et des priorités d’action.</div>
</div>
""")

    cols = st.columns(3)

    for col, (demo_key, demo) in zip(cols, DEMOS.items()):
        with col:
            html(f"""
<div class="premium-card">
<div>
<div class="card-label">{demo["label"]}</div>
<div class="card-title">{demo["title"]}</div>
<div class="card-subtitle">{demo["subtitle"]}</div>
</div>
<div class="card-story">{demo["story"]}</div>
</div>
""")

            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

            if st.button(demo["button"], key=f"demo_{demo_key}", use_container_width=True):
                try:
                    df = load_demo(demo_key)
                    load_analysis(df, demo_key)
                except Exception as e:
                    st.error(f"Impossible de charger cette démo : {e}")

    html("<div style='height:60px'></div>")

    render_monitoring_preview()

    html("<div style='height:70px'></div>")

    html("""
<div class="section-header">
<div class="section-kicker">MODE PRODUIT RÉEL</div>
<div class="section-title">Importer des verbatims clients</div>
<div class="section-description">Chargez des retours clients réels afin d’obtenir une lecture structurée des irritants, des sujets récurrents et des actions à prioriser.</div>
</div>
""")

    st.markdown("### Structure attendue des données")

    st.info(
        """
InsightIA analyse des données textuelles afin de détecter les irritants, les sujets récurrents, les parcours dégradés et les priorités d’action.

Le fichier CSV doit contenir au minimum une colonne de verbatim client : `text`, `commentaire`, `feedback`, `message` ou `avis`.

Colonnes recommandées : `date`, `canal`, `segment_client`, `region`, `parcours_client`, `score`.
"""
    )

    st.markdown("### Ce que générera InsightIA")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.success(
            """
**Lecture des frictions**

Sujets récurrents, irritants sensibles, signaux faibles et parcours dégradés.
"""
        )

    with c2:
        st.success(
            """
**Priorisation métier**

Niveaux d’attention, impact potentiel, récurrence et criticité des sujets.
"""
        )

    with c3:
        st.success(
            """
**Actions recommandées**

Actions prioritaires, équipes concernées, effort estimé et horizon conseillé.
"""
        )

    uploaded_file = st.file_uploader(
        "Déposer un fichier CSV",
        type=["csv"],
        label_visibility="visible",
    )

    if uploaded_file is not None:
        try:
            df = read_csv_robust(uploaded_file)

            st.success("Fichier chargé avec succès. Vous pouvez maintenant lancer l’analyse.")

            c1, c2, c3 = st.columns(3)
            c1.metric("Lignes détectées", f"{len(df):,}".replace(",", " "))
            c2.metric("Colonnes détectées", len(df.columns))
            c3.metric("Statut", "Prêt à analyser")

            st.markdown("### Aperçu des données importées")
            st.dataframe(df.head(20), use_container_width=True)

            st.markdown("### Lancer l’analyse")
            st.caption(
                "InsightIA va standardiser les colonnes, identifier les irritants et proposer une lecture structurée des priorités."
            )

            if st.button("Générer la lecture d’analyse", use_container_width=True):
                load_analysis(df, "Import CSV")

        except Exception as e:
            st.error(f"Erreur lors du chargement du fichier : {e}")


def render_page():
    page = st.session_state.page

    if page != "Accueil" and st.session_state.analysis_df is None:
        html("""
<div class="empty-state">
<div class="empty-kicker">ANALYSE NON INITIALISÉE</div>
<div class="empty-title">Commencez par lancer une démonstration.</div>
<div class="empty-text">Sélectionnez un environnement métier ou importez un fichier CSV pour activer l’analyse.</div>
</div>
""")

        if st.button("Retour à l’accueil"):
            go_to("Accueil")

        st.stop()

    if page == "Accueil":
        render_home()
    elif page == "Synthèse":
        render_executive()
    elif page == "Frictions détectées":
        render_explorer()
    elif page == "Priorisation":
        render_backlog()
    elif page == "Rapports":
        render_reports()


def main():
    init_state()
    render_header()
    render_navigation()
    html("<div style='height:38px'></div>")
    render_page()


if __name__ == "__main__":
    main()