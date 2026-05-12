# ui/pages/executive.py

import streamlit as st


def _top_value(df, column, default="Non disponible"):
    if column not in df.columns or df.empty:
        return default

    values = df[column].dropna()

    if values.empty:
        return default

    return values.astype(str).value_counts().idxmax()


def render_executive():
    df = st.session_state.analysis_df.copy()
    backlog = st.session_state.backlog_df.copy()

    st.markdown("## Centre d’intelligence")
    st.caption(
        "Lecture structurée des principaux sujets remontés par les clients."
    )

    total_feedbacks = len(df)

    negative_rate = round(
        df["sentiment"].eq("Négatif").mean() * 100,
        1,
    )

    blocking_cases = int(df["is_blocking"].sum())

    dominant_theme = _top_value(df, "theme")
    dominant_segment = _top_value(df, "segment_client")
    dominant_channel = _top_value(df, "channel")
    dominant_journey = _top_value(df, "parcours_client")

    st.markdown("### Synthèse")

    st.info(
        f"""
Les données analysées montrent une concentration importante des retours autour du sujet **{dominant_theme}**.

Les signaux les plus sensibles concernent principalement le segment **{dominant_segment}**, avec une forte présence des remontées via **{dominant_channel}**.

Le parcours le plus exposé semble être **{dominant_journey}**.
"""
    )

    st.markdown("### Vue d’ensemble")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Retours analysés",
        f"{total_feedbacks:,}".replace(",", " "),
    )

    c2.metric(
        "Niveau de risque expérience",
        "Élevé" if negative_rate > 45 else "Modéré",
    )

    c3.metric(
        "Frictions critiques détectées",
        blocking_cases,
    )

    c4.metric(
        "Sujet dominant",
        dominant_theme,
    )

    st.markdown("---")

    st.markdown("### Frictions nécessitant une attention")

    if backlog.empty:
        st.warning("Aucune priorité détectée.")
        return

    top_items = backlog.head(3)

    cols = st.columns(3)

    for col, (_, row) in zip(cols, top_items.iterrows()):

        theme = row.get("theme", "Sujet prioritaire")
        recommendation = row.get(
            "recommendation",
            "Définir un plan d’action ciblé.",
        )

        with col:
            with st.container(border=True):

                st.markdown(f"#### {theme}")

                st.markdown("**Constat**")

                st.write(
                    "Les retours analysés montrent une récurrence importante de cette friction dans l’expérience client."
                )

                st.markdown("**Impact observé**")

                st.write(
                    "Cette situation peut générer une perte de confiance, une augmentation des sollicitations support et une dégradation du parcours utilisateur."
                )

                st.markdown("**Action recommandée**")

                st.write(recommendation)

                st.caption(
                    "Priorité élevée · Recommandation opérationnelle"
                )

    st.markdown("---")

    st.markdown("### Sujets les plus récurrents")

    grouped = (
        df.groupby("theme")
        .size()
        .reset_index(name="Occurrences")
        .sort_values("Occurrences", ascending=False)
        .head(10)
    )

    st.dataframe(
        grouped,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    st.markdown("### Lecture opérationnelle")

    st.success(
        f"""
Les retours indiquent que les principales difficultés se concentrent actuellement autour du sujet **{dominant_theme}**.

Une amélioration du parcours **{dominant_journey}** pourrait réduire une partie importante des remontées négatives observées dans les données.
"""
    )