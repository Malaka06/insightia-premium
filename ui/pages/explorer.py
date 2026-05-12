import streamlit as st
import pandas as pd


def _safe_options(df, column):
    if column not in df.columns:
        return []

    return sorted(
        df[column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


def _top_value(df, column, default="Non disponible"):
    if column not in df.columns or df.empty:
        return default

    values = df[column].dropna()

    if values.empty:
        return default

    return values.astype(str).value_counts().idxmax()


def render_explorer():
    df = st.session_state.analysis_df.copy()

    st.markdown("## Frictions opérationnelles")

    st.caption(
        "Analyse des sujets récurrents remontés dans les retours clients."
    )

    st.markdown("### Affiner l’analyse")

    c1, c2, c3 = st.columns(3)

    with c1:
        selected_themes = st.multiselect(
            "Sujet",
            _safe_options(df, "theme"),
        )

    with c2:
        selected_segments = st.multiselect(
            "Segment",
            _safe_options(df, "segment_client"),
        )

    with c3:
        selected_channels = st.multiselect(
            "Canal",
            _safe_options(df, "channel"),
        )

    filtered = df.copy()

    if selected_themes:
        filtered = filtered[
            filtered["theme"].astype(str).isin(selected_themes)
        ]

    if selected_segments:
        filtered = filtered[
            filtered["segment_client"].astype(str).isin(selected_segments)
        ]

    if selected_channels:
        filtered = filtered[
            filtered["channel"].astype(str).isin(selected_channels)
        ]

    if filtered.empty:
        st.warning("Aucun résultat pour cette sélection.")
        return

    dominant_theme = _top_value(filtered, "theme")
    dominant_segment = _top_value(filtered, "segment_client")
    dominant_channel = _top_value(filtered, "channel")

    st.markdown("### Lecture des données")

    st.info(
        f"""
Les retours analysés montrent une forte présence des sujets liés à **{dominant_theme}**.

Les remontées concernent principalement le segment **{dominant_segment}** et proviennent majoritairement du canal **{dominant_channel}**.
"""
    )

    st.markdown("---")

    analytics_table = (
        filtered.groupby("theme")
        .agg({
            "text": "count",
            "segment_client": lambda x: x.mode()[0] if not x.mode().empty else "N/A",
            "channel": lambda x: x.mode()[0] if not x.mode().empty else "N/A",
        })
        .reset_index()
    )

    analytics_table.columns = [
        "Sujet",
        "Volume",
        "Segment dominant",
        "Canal dominant",
    ]

    st.markdown("### Vue analytique")

    st.dataframe(
        analytics_table,
        use_container_width=True,
        hide_index=True,
    )