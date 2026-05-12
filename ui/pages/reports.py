import streamlit as st
import pandas as pd

from core.exports import to_csv_bytes


def render_reports():
    analysis_df = st.session_state.analysis_df
    backlog_df = st.session_state.backlog_df

    st.markdown(
        """
        <div class="page-header">
            <div class="page-kicker">EXPORTS & PARTAGE</div>
            <div class="page-title">Rapports</div>
            <div class="page-description">
                Exportez les résultats d’analyse et les recommandations
                générées à partir des retours clients.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_feedbacks = len(analysis_df)

    negative_rate = round(
        analysis_df["sentiment"]
        .astype(str)
        .str.lower()
        .str.contains("négatif|negatif|negative", regex=True)
        .mean()
        * 100,
        1,
    )

    top_theme = (
        backlog_df.iloc[0]["theme"]
        if backlog_df is not None and len(backlog_df) > 0
        else "Aucun sujet détecté"
    )

    blocking_cases = (
        int(backlog_df["blocking_count"].sum())
        if backlog_df is not None and "blocking_count" in backlog_df.columns
        else 0
    )

    st.markdown("## Synthèse exécutive")

    st.info(
        f"""
InsightIA a analysé **{total_feedbacks} verbatims**.

Le principal sujet détecté concerne :
**{top_theme}**.

Le volume de retours négatifs représente
**{negative_rate}%** des verbatims analysés.

Nombre total de cas bloquants détectés :
**{blocking_cases}**.
"""
    )

    st.markdown("## Télécharger les résultats")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Télécharger l’analyse complète CSV",
            data=to_csv_bytes(analysis_df),
            file_name="insightia_analyse_complete.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            label="Télécharger les recommandations CSV",
            data=to_csv_bytes(backlog_df),
            file_name="insightia_recommandations.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("## Priorités recommandées")

    display_columns = [
        "theme",
        "priority",
        "priority_score",
        "recurrence_score",
        "negative_rate",
        "blocking_count",
        "expected_impact",
        "effort",
        "timeline",
        "teams",
        "recommendation",
    ]

    rename_columns = {
        "theme": "Sujet",
        "priority": "Niveau d’attention",
        "priority_score": "Score de priorité",
        "recurrence_score": "Récurrence",
        "negative_rate": "Taux négatif",
        "blocking_count": "Cas bloquants",
        "expected_impact": "Impact attendu",
        "effort": "Effort estimé",
        "timeline": "Horizon conseillé",
        "teams": "Équipes concernées",
        "recommendation": "Action recommandée",
    }

    available_columns = [
        col for col in display_columns
        if col in backlog_df.columns
    ]

    display_df = backlog_df[available_columns].rename(
        columns=rename_columns
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("## Méthodologie de lecture")

    st.success(
        """
Les sujets sont classés selon une logique de priorisation combinant :

- la récurrence du sujet dans les retours analysés
- le taux de retours négatifs
- le nombre de cas bloquants détectés
- le niveau moyen de criticité
- l’impact potentiel sur le parcours client

L’objectif n’est pas seulement d’identifier des problèmes,
mais de transformer les verbatims clients en priorités d’action.
"""
    )