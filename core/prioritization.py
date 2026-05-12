import pandas as pd


RECOMMENDATIONS = {
    "Livraison / Logistique": "Améliorer le suivi de livraison, clarifier les délais et renforcer les notifications proactives.",
    "Support client": "Réduire les délais de réponse et améliorer le suivi des demandes récurrentes.",
    "Remboursement / Facturation": "Clarifier les remboursements, les factures et les délais de traitement.",
    "Facturation / Pricing": "Clarifier la tarification, les options facturées et les règles de renouvellement.",
    "Produit / Qualité": "Identifier les défauts récurrents et prioriser les corrections ayant le plus d’impact client.",
    "Onboarding / Usage": "Simplifier les premières étapes d’usage et améliorer l’accompagnement utilisateur.",
    "Démarches administratives": "Clarifier les procédures, réduire les délais et améliorer le suivi des dossiers.",
    "Communication": "Renforcer la clarté des messages, les notifications et la visibilité sur l’avancement.",
    "Accueil / Support usager": "Améliorer l’orientation, la continuité de suivi et la clarté des réponses.",
    "Paiement / Frais consulaires": "Clarifier les frais, les reçus et les modalités de paiement.",
    "Digitalisation / Suivi en ligne": "Mettre en place un meilleur suivi en ligne et des confirmations automatiques.",
    "Autre / Non classé": "Analyser manuellement les retours non classés pour enrichir la taxonomie.",
}


TEAMS = {
    "Livraison / Logistique": "Logistique · Support · Expérience client",
    "Support client": "Support · Expérience client · Opérations",
    "Remboursement / Facturation": "Finance · Support · Opérations",
    "Facturation / Pricing": "Finance · Produit · Relation client",
    "Produit / Qualité": "Produit · Qualité · Support",
    "Onboarding / Usage": "Produit · Customer Success · Support",
    "Démarches administratives": "Opérations · Accueil · Communication",
    "Communication": "Communication · Support · Opérations",
    "Accueil / Support usager": "Accueil · Support · Opérations",
    "Paiement / Frais consulaires": "Finance · Accueil · Opérations",
    "Digitalisation / Suivi en ligne": "Produit · Digital · Opérations",
    "Autre / Non classé": "Équipe métier · Analyse · Opérations",
}


def priority_label(score: float) -> str:
    if score >= 70:
        return "Priorité élevée"
    if score >= 45:
        return "Sous surveillance"
    return "Impact modéré"


def expected_impact(score: float) -> str:
    if score >= 70:
        return "Élevé"
    if score >= 45:
        return "Moyen"
    return "Modéré"


def effort_level(theme: str) -> str:
    if theme in ["Communication", "Support client", "Accueil / Support usager"]:
        return "Faible à moyen"
    if theme in ["Digitalisation / Suivi en ligne", "Produit / Qualité"]:
        return "Moyen à élevé"
    return "Moyen"


def action_horizon(score: float) -> str:
    if score >= 70:
        return "30 jours"
    if score >= 45:
        return "30 à 60 jours"
    return "À suivre"


def build_backlog(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()

    rows = []
    total = max(1, len(df))

    for theme, group in df.groupby("theme"):
        volume = len(group)
        recurrence_score = (volume / total) * 100

        negative_rate = (
            group["sentiment"].eq("Négatif").mean() * 100
            if "sentiment" in group.columns
            else 0
        )

        blocking_count = int(group["is_blocking"].sum()) if "is_blocking" in group.columns else 0
        blocking_rate = (blocking_count / max(1, volume)) * 100

        avg_severity = (
            float(group["severity_score"].mean())
            if "severity_score" in group.columns
            else 1
        )

        priority_score = (
            recurrence_score * 0.35
            + negative_rate * 0.30
            + blocking_rate * 0.20
            + avg_severity * 10 * 0.15
        )

        priority_score = round(priority_score, 2)

        rows.append(
            {
                "theme": theme,
                "volume": volume,
                "negative_rate": round(negative_rate, 1),
                "blocking_count": blocking_count,
                "avg_severity": round(avg_severity, 2),
                "priority_score": priority_score,
                "priority": priority_label(priority_score),
                "expected_impact": expected_impact(priority_score),
                "effort": effort_level(theme),
                "timeline": action_horizon(priority_score),
                "teams": TEAMS.get(theme, "Équipe métier · Opérations"),
                "recommendation": RECOMMENDATIONS.get(
                    theme,
                    "Définir un plan d’action ciblé à partir des retours récurrents.",
                ),
            }
        )

    backlog = pd.DataFrame(rows)

    if backlog.empty:
        return backlog

    order = {
        "Priorité élevée": 0,
        "Sous surveillance": 1,
        "Impact modéré": 2,
    }

    backlog["priority_rank"] = backlog["priority"].map(order).fillna(3)

    backlog = backlog.sort_values(
        by=["priority_rank", "priority_score", "volume"],
        ascending=[True, False, False],
    ).drop(columns=["priority_rank"])

    return backlog.reset_index(drop=True)