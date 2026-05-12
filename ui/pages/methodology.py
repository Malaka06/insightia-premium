import streamlit as st


def render_methodology():
    st.markdown("## Méthodologie analytique")

    st.caption(
        "Cette page explique comment InsightIA transforme des verbatims clients en priorités d’action."
    )

    st.markdown("### Pipeline d’analyse")

    st.info(
        """
1. Import des retours clients  
2. Standardisation des colonnes  
3. Nettoyage du texte  
4. Détection des thèmes métier  
5. Analyse du sentiment  
6. Identification des cas bloquants  
7. Calcul des scores  
8. Priorisation opérationnelle  
9. Génération des recommandations
"""
    )

    st.markdown("---")

    st.markdown("### Logique de classification")

    st.write(
        """
InsightIA utilise une taxonomie métier explicable.  
Chaque retour est associé à un thème selon les mots-clés détectés dans le verbatim.
"""
    )

    taxonomy_examples = [
        {"Mot-clé détecté": "retard, colis, livraison", "Thème": "Livraison / Logistique"},
        {"Mot-clé détecté": "support, réponse, attente", "Thème": "Support client"},
        {"Mot-clé détecté": "remboursement, facture, paiement", "Thème": "Remboursement / Facturation"},
        {"Mot-clé détecté": "bug, qualité, fonctionne", "Thème": "Produit / Qualité"},
        {"Mot-clé détecté": "connexion, interface, documentation", "Thème": "Onboarding / Usage"},
    ]

    st.dataframe(
        taxonomy_examples,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    st.markdown("### Score de priorité")

    st.write(
        """
Le score de priorité combine plusieurs dimensions afin de ne pas classer les sujets uniquement par volume.
"""
    )

    st.code(
        """
priority_score =
    recurrence_score * 0.45
    + negative_rate * 0.30
    + blocking_rate * 0.15
    + avg_severity * 12
""",
        language="python",
    )

    st.markdown("### Dimensions utilisées")

    scoring_table = [
        {"Dimension": "Récurrence", "Rôle": "Mesure le poids du sujet dans l’ensemble des retours."},
        {"Dimension": "Taux négatif", "Rôle": "Mesure la part de retours exprimant une insatisfaction."},
        {"Dimension": "Cas bloquants", "Rôle": "Identifie les retours qui empêchent l’utilisateur d’avancer."},
        {"Dimension": "Criticité moyenne", "Rôle": "Renforce les sujets combinant sentiment négatif, blocage et signaux forts."},
    ]

    st.dataframe(
        scoring_table,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    st.markdown("### Niveaux de priorité")

    priority_table = [
        {"Score": "≥ 45", "Niveau": "Priorité élevée", "Horizon": "7 à 30 jours"},
        {"Score": "28 à 44", "Niveau": "Sous surveillance", "Horizon": "30 à 60 jours"},
        {"Score": "< 28", "Niveau": "Impact modéré", "Horizon": "Surveillance continue"},
    ]

    st.dataframe(
        priority_table,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    st.markdown("### Gouvernance analytique")

    st.success(
        """
InsightIA privilégie une approche explicable :

- les thèmes sont basés sur une taxonomie métier contrôlable ;
- les scores sont visibles et interprétables ;
- les recommandations sont reliées aux irritants détectés ;
- les verbatims restent accessibles comme preuves qualitatives ;
- l’objectif est d’aider à prioriser, pas de remplacer la décision humaine.
"""
    )