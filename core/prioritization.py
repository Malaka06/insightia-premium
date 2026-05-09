import pandas as pd


RECOMMENDATIONS = {
    "Livraison / Logistique": "Améliorer le suivi logistique et les délais de livraison.",
    "Support client": "Réduire les délais de réponse du support.",
    "Remboursement / Facturation": "Clarifier les remboursements et la facturation.",
    "Produit / Qualité": "Analyser les défauts produits récurrents.",
    "Onboarding / Usage": "Simplifier l’onboarding utilisateur.",
    "Démarches administratives": "Réduire les délais administratifs.",
    "Communication": "Clarifier les procédures et la communication.",
    "Autre / Non classé": "Analyser les verbatims non classés.",
}


def assign_priority(score):
    if score >= 70:
        return "P0"
    elif score >= 50:
        return "P1"
    elif score >= 30:
        return "P2"
    return "P3"


def build_backlog(df: pd.DataFrame):

    grouped = (
        df.groupby("theme")
        .agg(
            volume=("theme", "count"),
            negative_rate=("sentiment", lambda x: (x == "Négatif").mean() * 100),
            blocking_count=("is_blocking", "sum"),
            avg_severity=("severity_score", "mean"),
        )
        .reset_index()
    )

    grouped["priority_score"] = (
        grouped["volume"] * 0.35
        + grouped["negative_rate"] * 0.30
        + grouped["blocking_count"] * 8
        + grouped["avg_severity"] * 10
    )

    grouped["priority"] = grouped["priority_score"].apply(assign_priority)

    grouped["recommendation"] = grouped["theme"].map(
        lambda x: RECOMMENDATIONS.get(
            x,
            "Définir un plan d’action adapté."
        )
    )

    grouped = grouped.sort_values(
        by="priority_score",
        ascending=False
    )

    return grouped.reset_index(drop=True)