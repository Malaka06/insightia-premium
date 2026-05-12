# ui/pages/explorer.py

import streamlit as st


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

    st.markdown("### Sujets les plus remontés")

    grouped = (
        filtered.groupby("theme")
        .size()
        .reset_index(name="Occurrences")
        .sort_values("Occurrences", ascending=False)
    )

    for _, row in grouped.head(6).iterrows():

        subset = filtered[
            filtered["theme"] == row["theme"]
        ]

        top_irritant = _top_value(
            subset,
            "irritant",
            row["theme"],
        )

        with st.container(border=True):

            st.markdown(f"#### {row['theme']}")

            st.write(
                f"**Sujet récurrent :** {top_irritant}"
            )

            st.write(
                f"**Volume observé :** {row['Occurrences']} retours"
            )

            st.write(
                "Ce sujet apparaît de manière répétée dans les verbatims analysés."
            )

    st.markdown("---")

    st.markdown("### Expressions fréquemment retrouvées")

    if "irritant" in filtered.columns:

        recurring = (
            filtered["irritant"]
            .dropna()
            .astype(str)
            .value_counts()
            .head(12)
            .reset_index()
        )

        recurring.columns = [
            "Expression détectée",
            "Occurrences",
        ]

        st.dataframe(
            recurring,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("---")

    st.markdown("### Aperçu des retours analysés")

    columns = [
        "date",
        "segment_client",
        "channel",
        "theme",
        "irritant",
        "text",
    ]

    existing = [
        col for col in columns
        if col in filtered.columns
    ]

    st.dataframe(
        filtered[existing].head(250),
        use_container_width=True,
        hide_index=True,
        height=520,
    )