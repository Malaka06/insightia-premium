import streamlit as st
import pandas as pd


def _top_value(df, column, default="Non disponible"):
    if column not in df.columns or df.empty:
        return default

    values = df[column].dropna()
    if values.empty:
        return default

    return values.value_counts().idxmax()


def render_executive():
    df = st.session_state.analysis_df.copy()
    backlog = st.session_state.backlog_df.copy()

    total = len(df)

    top_theme = _top_value(df, "theme")
    top_segment = _top_value(df, "segment_client")
    top_channel = _top_value(df, "channel")
    top_region = _top_value(df, "region")
    top_journey = _top_value(df, "parcours_client")

    negative_rate = round(df["sentiment"].eq("Négatif").mean() * 100, 1)
    blocking_count = int(df["is_blocking"].sum())

    if "urgency" in df.columns:
        critical_count = int(df["urgency"].isin(["Critique", "Élevée"]).sum())
    else:
        critical_count = 0

    risk_score = min(
        100,
        round(
            negative_rate * 0.45
            + (blocking_count / max(total, 1) * 100) * 0.35
            + (critical_count / max(total, 1) * 100) * 0.20
        ),
    )

    if risk_score >= 70:
        risk_level = "ÉLEVÉ"
        priority = "P0"
    elif risk_score >= 50:
        risk_level = "MODÉRÉ"
        priority = "P1"
    else:
        risk_level = "SOUS CONTRÔLE"
        priority = "P2"

    st.markdown("## Centre d’Intelligence")
    st.caption(
        "Vue exécutive des risques clients, des segments exposés et des priorités opérationnelles."
    )

    st.markdown("### Résumé stratégique IA")

    st.info(
        f"L’analyse de **{total:,} verbatims** montre que la friction dominante concerne "
        f"**{top_theme}**. Le taux de retours négatifs est de **{negative_rate}%**. "
        f"Le segment le plus exposé est **{top_segment}**, principalement via **{top_channel}**. "
        f"La priorité décisionnelle recommandée est **{priority}**."
    )

    st.markdown("### Indicateurs décisionnels")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Risque expérience",
        risk_level,
        help="Niveau global de dégradation de l’expérience client détecté dans les verbatims.",
    )

    c2.metric(
        "Priorité décisionnelle",
        priority,
        help="Niveau de priorité calculé à partir du taux négatif, des cas bloquants et de la criticité.",
    )

    c3.metric(
        "Cas bloquants",
        blocking_count,
        help="Nombre de situations où le client ou l’usager ne peut pas avancer normalement.",
    )

    c4.metric(
        "Segment exposé",
        top_segment,
        help="Segment client le plus représenté dans les irritants détectés.",
    )

    st.markdown("---")

    st.markdown("### Observations stratégiques")

    if backlog is None or backlog.empty:
        st.warning("Aucune priorité détectée pour le moment.")
    else:
        top_backlog = backlog.head(3)
        cols = st.columns(3)

        for col, (_, row) in zip(cols, top_backlog.iterrows()):
            with col:
                st.markdown(f"#### {row.get('priority', 'P?')} — {row.get('theme', 'Sujet prioritaire')}")
                st.write(f"**Volume détecté :** {row.get('volume', 0)}")
                st.write(f"**Taux négatif :** {row.get('negative_rate', 0)}%")
                st.write(f"**Cas bloquants :** {row.get('blocking_count', 0)}")
                st.write(f"**Action recommandée :** {row.get('recommendation', 'Définir un plan d’action ciblé.')}")

    st.markdown("---")

    st.markdown("### Lecture opérationnelle")

    left, right = st.columns([1.2, 0.8])

    with left:
        if "theme" in df.columns:
            theme_table = (
                df.groupby("theme")
                .agg(
                    volume=("theme", "count"),
                    taux_negatif=("sentiment", lambda x: round(x.eq("Négatif").mean() * 100, 1)),
                    cas_bloquants=("is_blocking", "sum"),
                    urgence_moyenne=("severity_score", "mean"),
                )
                .reset_index()
                .sort_values(
                    ["cas_bloquants", "taux_negatif", "volume"],
                    ascending=False,
                )
                .head(10)
            )

            st.dataframe(
                theme_table,
                use_container_width=True,
                hide_index=True,
            )

    with right:
        st.markdown("#### Recommandation exécutive")

        st.success(
            f"Traiter en priorité **{top_theme}** sur le parcours **{top_journey}**. "
            f"L’objectif n’est pas seulement de réduire les commentaires négatifs, "
            f"mais de restaurer la confiance opérationnelle."
        )

        st.write(f"**Impact attendu :** Élevé")
        st.write(f"**Effort estimé :** Moyen")
        st.write(f"**Horizon :** 30 jours")
        st.write(f"**Équipes concernées :** CX · Produit · Ops")
        st.write(f"**Zone exposée :** {top_region}")