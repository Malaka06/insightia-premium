import streamlit as st


def render_backlog():
    backlog_df = st.session_state.backlog_df

    st.markdown("## Prioritization Board")
    st.caption("Backlog business généré à partir des irritants détectés dans les verbatims.")

    if backlog_df is None or backlog_df.empty:
        st.warning("Aucun backlog disponible. Lancez d’abord une démo ou une analyse CSV.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Sujets priorisés", len(backlog_df))
    c2.metric("Priorités P0", int((backlog_df["priority"] == "P0").sum()))
    c3.metric("Priorités P1", int((backlog_df["priority"] == "P1").sum()))

    st.markdown("### Backlog priorisé")

    columns_to_show = [
        "priority",
        "theme",
        "volume",
        "negative_rate",
        "blocking_count",
        "avg_severity",
        "priority_score",
        "recommendation",
    ]

    existing_columns = [col for col in columns_to_show if col in backlog_df.columns]

    st.dataframe(
        backlog_df[existing_columns],
        use_container_width=True,
        height=450,
    )

    st.markdown("### Lecture business")

    top = backlog_df.iloc[0]

    st.info(
        f"La priorité principale est **{top['theme']}** avec un score de priorité de "
        f"**{round(float(top['priority_score']), 2)}**. "
        f"Action recommandée : **{top['recommendation']}**."
    )