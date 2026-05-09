import streamlit as st


def _top_value(df, column, default="Non disponible"):
    if column not in df.columns or df.empty:
        return default
    values = df[column].dropna()
    if values.empty:
        return default
    return values.value_counts().idxmax()


def _safe_options(df, column):
    if column not in df.columns:
        return []
    return sorted(df[column].dropna().astype(str).unique())


def render_explorer():
    df = st.session_state.analysis_df.copy()

    st.markdown("## Frictions Opérationnelles")
    st.caption(
        "Analyse des irritants clients, des segments exposés, des canaux de remontée et des parcours les plus sensibles."
    )

    st.markdown("### Affiner l’analyse")

    c1, c2, c3 = st.columns(3)

    with c1:
        themes = st.multiselect("Friction opérationnelle", _safe_options(df, "theme"))

    with c2:
        segments = st.multiselect("Segment exposé", _safe_options(df, "segment_client"))

    with c3:
        channels = st.multiselect("Canal de remontée", _safe_options(df, "channel"))

    c4, c5, c6 = st.columns(3)

    with c4:
        urgencies = st.multiselect("Niveau d’urgence", _safe_options(df, "urgency"))

    with c5:
        regions = st.multiselect("Région", _safe_options(df, "region"))

    with c6:
        journeys = st.multiselect("Parcours concerné", _safe_options(df, "parcours_client"))

    filtered = df.copy()

    if themes:
        filtered = filtered[filtered["theme"].astype(str).isin(themes)]
    if segments:
        filtered = filtered[filtered["segment_client"].astype(str).isin(segments)]
    if channels:
        filtered = filtered[filtered["channel"].astype(str).isin(channels)]
    if urgencies:
        filtered = filtered[filtered["urgency"].astype(str).isin(urgencies)]
    if regions:
        filtered = filtered[filtered["region"].astype(str).isin(regions)]
    if journeys:
        filtered = filtered[filtered["parcours_client"].astype(str).isin(journeys)]

    if filtered.empty:
        st.warning("Aucune friction ne correspond aux filtres sélectionnés.")
        return

    total = len(filtered)
    top_theme = _top_value(filtered, "theme")
    top_segment = _top_value(filtered, "segment_client")
    top_channel = _top_value(filtered, "channel")
    top_region = _top_value(filtered, "region")
    top_journey = _top_value(filtered, "parcours_client")

    negative_rate = round(filtered["sentiment"].eq("Négatif").mean() * 100, 1)
    blocking_count = int(filtered["is_blocking"].sum())

    if "urgency" in filtered.columns:
        critical_count = int(filtered["urgency"].isin(["Critique", "Élevée"]).sum())
    else:
        critical_count = 0

    st.markdown("### Lecture décisionnelle")

    st.info(
        f"La friction dominante est **{top_theme}**. "
        f"Sur le périmètre analysé, **{negative_rate}%** des retours sont négatifs "
        f"et **{blocking_count}** cas bloquants ont été identifiés. "
        f"Le segment le plus exposé est **{top_segment}**, principalement via **{top_channel}**."
    )

    st.markdown("### Indicateurs de friction")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Frictions analysées", f"{total:,}".replace(",", " "))
    m2.metric("Taux négatif", f"{negative_rate}%")
    m3.metric("Signaux critiques", critical_count)
    m4.metric("Cas bloquants", blocking_count)

    st.markdown("---")

    st.markdown("### Frictions prioritaires")

    grouped = (
        filtered.groupby("theme")
        .agg(
            volume=("theme", "count"),
            taux_negatif=("sentiment", lambda x: round(x.eq("Négatif").mean() * 100, 1)),
            cas_bloquants=("is_blocking", "sum"),
            urgence_moyenne=("severity_score", "mean"),
        )
        .reset_index()
        .sort_values(["cas_bloquants", "taux_negatif", "volume"], ascending=False)
        .head(6)
    )

    for _, row in grouped.iterrows():
        theme = row["theme"]
        subset = filtered[filtered["theme"] == theme]

        irritant = _top_value(subset, "irritant", theme)
        segment = _top_value(subset, "segment_client")
        channel = _top_value(subset, "channel")
        impact = _top_value(subset, "impact_business", "Impact client et opérationnel")

        with st.container(border=True):
            st.markdown(f"#### {theme}")
            st.write(f"**Irritant récurrent :** {irritant}")
            st.write(f"**Segment exposé :** {segment}")
            st.write(f"**Canal dominant :** {channel}")
            st.write(f"**Impact business :** {impact}")
            st.write(
                f"**Volume :** {int(row['volume'])} · "
                f"**Taux négatif :** {row['taux_negatif']}% · "
                f"**Cas bloquants :** {int(row['cas_bloquants'])}"
            )

    st.markdown("---")

    st.markdown("### Langage client récurrent")

    if "irritant" in filtered.columns:
        expressions = filtered["irritant"].dropna().astype(str).value_counts().head(10)
        st.dataframe(
            expressions.reset_index().rename(
                columns={"index": "Expression récurrente", "irritant": "Volume"}
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("---")

    st.markdown("### Verbatims à l’origine des décisions")

    columns = [
        "date",
        "segment_client",
        "channel",
        "region",
        "parcours_client",
        "theme",
        "irritant",
        "urgency",
        "impact_business",
        "text",
    ]

    existing = [col for col in columns if col in filtered.columns]

    st.dataframe(
        filtered[existing].head(300),
        use_container_width=True,
        hide_index=True,
        height=520,
    )