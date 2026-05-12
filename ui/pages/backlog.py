# ui/pages/backlog.py

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

            priority_reasons = []

            if row["volume"] > 200:
                priority_reasons.append("volume élevé")

            if row["negative_rate"] > 60:
                priority_reasons.append("forte négativité")

            if row["blocking_count"] > 20:
                priority_reasons.append("nombre important de cas bloquants")

            st.markdown("**Pourquoi ce sujet est prioritaire**")

            st.info(" • ".join(priority_reasons))

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