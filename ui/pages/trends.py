import streamlit as st
import pandas as pd


def render_trends():
    df = st.session_state.analysis_df.copy()

    st.markdown("## Tendances & signaux faibles")

    st.caption(
        "Suivi de l’évolution des irritants clients et détection des sujets émergents."
    )

    if df is None or df.empty:
        st.warning("Aucune donnée disponible.")
        return

    if "date" not in df.columns:
        st.info(
            """
Aucune colonne date n’a été détectée dans les données.  
La page affiche donc une lecture par volume global plutôt qu’une évolution temporelle.
"""
        )

        trend_table = (
            df.groupby("theme")
            .size()
            .reset_index(name="Volume")
            .sort_values("Volume", ascending=False)
        )

        st.markdown("### Sujets dominants")

        st.dataframe(
            trend_table,
            use_container_width=True,
            hide_index=True,
        )

        return

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    if df.empty:
        st.warning("Les dates n’ont pas pu être interprétées.")
        return

    df["week"] = df["date"].dt.to_period("W").astype(str)

    st.markdown("### Évolution hebdomadaire des irritants")

    weekly = (
        df.groupby(["week", "theme"])
        .size()
        .reset_index(name="Volume")
        .sort_values("week")
    )

    st.line_chart(
        weekly,
        x="week",
        y="Volume",
        color="theme",
        use_container_width=True,
    )

    st.markdown("---")

    st.markdown("### Sujets en progression")

    theme_volume = (
        weekly.groupby("theme")["Volume"]
        .sum()
        .reset_index()
        .sort_values("Volume", ascending=False)
    )

    st.dataframe(
        theme_volume,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    st.markdown("### Signaux faibles détectés")

    signal_table = (
        df.groupby("theme")
        .agg(
            volume=("text", "count"),
            negative_rate=(
                "sentiment",
                lambda x: round(
                    x.astype(str)
                    .str.lower()
                    .str.contains("négatif|negatif|negative", regex=True)
                    .mean()
                    * 100,
                    1,
                ),
            ),
            blocking_count=("is_blocking", "sum"),
        )
        .reset_index()
    )

    weak_signals = signal_table[
        (signal_table["volume"] < signal_table["volume"].median())
        & (
            (signal_table["negative_rate"] >= 40)
            | (signal_table["blocking_count"] >= 1)
        )
    ].sort_values(
        ["negative_rate", "blocking_count"],
        ascending=False,
    )

    if weak_signals.empty:
        st.success(
            "Aucun signal faible critique détecté pour le moment."
        )
    else:
        st.warning(
            "Certains sujets restent encore peu volumineux, mais présentent déjà des signaux de risque."
        )

        st.dataframe(
            weak_signals,
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("---")

    st.markdown("### Lecture décisionnelle")

    top_theme = (
        theme_volume.iloc[0]["theme"]
        if not theme_volume.empty
        else "Non disponible"
    )

    st.success(
        f"""
Le sujet le plus visible dans la période analysée est **{top_theme}**.

Cette page permet de distinguer :
- les irritants déjà dominants ;
- les sujets émergents ;
- les signaux faibles à surveiller ;
- les thématiques qui peuvent nécessiter une action avant qu’elles ne deviennent critiques.
"""
    )