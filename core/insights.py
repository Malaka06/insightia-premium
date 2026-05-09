def executive_summary(df, backlog, demo_name="InsightIA"):
    if df is None or df.empty:
        return "Aucune donnée analysée pour le moment."
    total = len(df)
    neg = int((df["sentiment"] == "Négatif").sum())
    neg_rate = round(neg / total * 100, 1) if total else 0
    if backlog is not None and not backlog.empty:
        top = backlog.iloc[0]
        return (
            f"{demo_name} révèle que le sujet prioritaire est « {top['theme']} », "
            f"avec {top['volume_share']}% des verbatims analysés. "
            f"Le taux de verbatims négatifs atteint {neg_rate}%, ce qui indique une zone d’attention "
            f"à traiter en priorité pour réduire la friction client et améliorer l’expérience globale."
        )
    return f"{demo_name} a analysé {total} verbatims. Le taux de verbatims négatifs est de {neg_rate}%."
