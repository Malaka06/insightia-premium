import streamlit as st


def render_backlog():
    backlog_df = st.session_state.backlog_df

    st.markdown("## Moteur de priorisation")
    st.caption(
        "Les sujets sont classés selon leur récurrence, leur criticité, leur impact potentiel et les cas bloquants détectés."
    )

    if backlog_df is None or backlog_df.empty:
        st.warning("Aucune priorité disponible. Lancez d’abord une démo ou importez un fichier.")
        return

    high_count = int((backlog_df["priority"] == "Priorité élevée").sum())
    watch_count = int((backlog_df["priority"] == "Sous surveillance").sum())
    moderate_count = int((backlog_df["priority"] == "Impact modéré").sum())

    c1, c2, c3 = st.columns(3)

    c1.metric("Priorités élevées", high_count)
    c2.metric("Sujets sous surveillance", watch_count)
    c3.metric("Impacts modérés", moderate_count)

    st.markdown("---")

    st.markdown("### Sujets nécessitant une décision")

    for _, row in backlog_df.head(8).iterrows():
        with st.container(border=True):
            st.markdown(f"### {row['theme']}")
            st.caption(row["priority"])

            st.markdown("**Pourquoi ce sujet remonte**")
            st.write(
                f"Ce sujet apparaît dans **{row['volume']} retours**. "
                f"Il présente un taux de retours négatifs de **{row['negative_rate']}%** "
                f"et **{row['blocking_count']} cas bloquants**."
            )

            st.markdown("**Impact potentiel**")
            st.write(
                f"Impact attendu : **{row['expected_impact']}**. "
                f"Ce sujet peut dégrader la confiance, augmenter les sollicitations support "
                f"ou ralentir le parcours client."
            )

            st.markdown("**Action recommandée**")
            st.write(row["recommendation"])

            c1, c2, c3 = st.columns(3)
            c1.write(f"**Effort estimé :** {row['effort']}")
            c2.write(f"**Horizon :** {row['timeline']}")
            c3.write(f"**Équipes :** {row['teams']}")

    st.markdown("---")

    st.markdown("### Vue structurée des priorités")

    columns = [
        "priority",
        "theme",
        "volume",
        "negative_rate",
        "blocking_count",
        "expected_impact",
        "effort",
        "timeline",
        "teams",
        "recommendation",
    ]

    existing = [col for col in columns if col in backlog_df.columns]

    st.dataframe(
        backlog_df[existing],
        use_container_width=True,
        hide_index=True,
        height=480,
    )