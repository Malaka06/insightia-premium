import streamlit as st


def render_reports():
    df = st.session_state.analysis_df
    backlog_df = st.session_state.backlog_df

    st.markdown("## Reports")
    st.caption("Exportez les résultats d’analyse et le backlog priorisé.")

    if df is None:
        st.warning("Aucune analyse disponible.")
        return

    st.markdown("### Synthèse exécutive")

    total = len(df)
    negative_rate = round(df["sentiment"].eq("Négatif").mean() * 100, 1)
    blocking_count = int(df["is_blocking"].sum())
    top_theme = df["theme"].value_counts().idxmax()

    st.info(
        f"InsightIA a analysé **{total} verbatims**. "
        f"Le taux de retours négatifs est de **{negative_rate}%**. "
        f"Le principal irritant détecté est **{top_theme}**. "
        f"Nombre d’incidents bloquants : **{blocking_count}**."
    )

    st.markdown("### Télécharger les résultats")

    analysis_csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Télécharger l’analyse complète CSV",
        data=analysis_csv,
        file_name="insightia_analysis.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if backlog_df is not None and not backlog_df.empty:
        backlog_csv = backlog_df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="Télécharger le backlog priorisé CSV",
            data=backlog_csv,
            file_name="insightia_backlog.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown("### Backlog aperçu")
        st.dataframe(backlog_df, use_container_width=True)