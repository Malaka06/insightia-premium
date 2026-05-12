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
        "Lecture stratégique des principaux irritants détectés dans les retours clients."
    )

    total_feedbacks = len(df)

    negative_rate = round(
        df["sentiment"]
        .astype(str)
        .str.lower()
        .str.contains("négatif|negatif|negative", regex=True)
        .mean()
        * 100,
        1,
    )

    blocking_cases = int(df["is_blocking"].sum())

    dominant_theme = _top_value(df, "theme")
    dominant_segment = _top_value(df, "segment_client")
    dominant_channel = _top_value(df, "channel")
    dominant_journey = _top_value(df, "parcours_client")

    st.markdown("### Synthèse exécutive")

    st.info(
        f"""
Les données analysées montrent une concentration importante des retours autour du sujet **{dominant_theme}**.

Les remontées concernent principalement le segment **{dominant_segment}** et proviennent majoritairement du canal **{dominant_channel}**.

Le parcours client actuellement le plus exposé semble être **{dominant_journey}**.
"""
    )

    st.markdown("### Vue d’ensemble")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Retours analysés",
        f"{total_feedbacks:,}".replace(",", " "),
        help="Nombre total de verbatims analysés dans le périmètre sélectionné.",
    )

    c2.metric(
        "Taux négatif",
        f"{negative_rate}%",
        help="Part des retours exprimant une insatisfaction ou une frustration.",
    )

    c3.metric(
        "Cas bloquants",
        blocking_cases,
        help="Nombre de retours identifiés comme fortement bloquants pour l’expérience client.",
    )

    c4.metric(
        "Sujet dominant",
        dominant_theme,
        help="Sujet apparaissant le plus fréquemment dans les retours analysés.",
    )

    st.markdown("---")

    st.markdown("### Insights exécutifs")

    top_priority = (
        backlog.iloc[0]["theme"]
        if not backlog.empty
        else "Aucun sujet"
    )

    top_team = (
        backlog.iloc[0]["teams"]
        if not backlog.empty and "teams" in backlog.columns
        else "Équipe métier"
    )

    top_action = (
        backlog.iloc[0]["recommendation"]
        if not backlog.empty and "recommendation" in backlog.columns
        else "Définir un plan d’action."
    )

    e1, e2 = st.columns(2)

    with e1:
        st.error(
            f"""
### Risque principal détecté

Le sujet **{top_priority}** concentre actuellement la majorité des remontées critiques.

Cette situation peut :
- augmenter les sollicitations support,
- ralentir certains parcours clients,
- dégrader la confiance utilisateur,
- générer des abandons ou du churn.
"""
        )

    with e2:
        st.success(
            f"""
### Action prioritaire recommandée

Équipes concernées :
**{top_team}**

Action recommandée :
**{top_action}**

Horizon conseillé :
**7 à 30 jours**
"""
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

        volume = row.get("volume", 0)

        negative_rate_row = row.get("negative_rate", 0)

        blocking_count = row.get("blocking_count", 0)

        priority_score = row.get("priority_score", 0)

        with col:
            with st.container(border=True):

                st.markdown(f"#### {theme}")

                st.caption(
                    f"Score de priorité : {priority_score}"
                )

                st.markdown("**Constat analytique**")

                st.write(
                    f"""
Ce sujet représente actuellement **{volume} retours** avec :

- **{negative_rate_row}%** de retours négatifs
- **{blocking_count} cas bloquants détectés**
"""
                )

                st.markdown("**Impact business potentiel**")

                st.write(
                    """
Cette friction peut :
- augmenter les tickets support,
- ralentir l’expérience utilisateur,
- dégrader la satisfaction,
- réduire la confiance client.
"""
                )

                st.markdown("**Exemples de verbatims détectés**")

                if "text" in df.columns:

                    theme_examples = (
                        df[df["theme"] == theme]["text"]
                        .dropna()
                        .drop_duplicates()
                        .head(3)
                        .tolist()
                    )

                    if theme_examples:

                        for example in theme_examples:

                            st.markdown(
                                f"""
                                <div style="
                                    padding:12px;
                                    border-radius:12px;
                                    background:#111827;
                                    margin-bottom:8px;
                                    border:1px solid rgba(255,255,255,0.08);
                                ">
                                “{example}”
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    else:
                        st.caption(
                            "Aucun verbatim disponible pour ce sujet."
                        )

                else:
                    st.caption(
                        "Colonne texte non disponible."
                    )

                st.markdown("**Action recommandée**")

                st.write(recommendation)

    st.markdown("---")

    st.markdown("### Vue analytique des sujets")

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
Les retours analysés indiquent que les principales difficultés se concentrent actuellement autour du sujet **{dominant_theme}**.

Une amélioration du parcours **{dominant_journey}** pourrait réduire une part importante des remontées négatives observées dans les données.

Les signaux détectés suggèrent qu’une action ciblée sur ce périmètre pourrait améliorer l’expérience client et réduire les frictions opérationnelles.
"""
    )