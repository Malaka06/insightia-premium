from __future__ import annotations
import pandas as pd


def executive_kpis(df: pd.DataFrame) -> dict:
    total = len(df)
    negative = int((df["sentiment"] == "Négatif").sum())
    blocking = int(df["is_blocking"].sum())
    top_theme = df["theme"].value_counts().index[0] if total else "N/A"
    return {
        "feedbacks": total,
        "negative_rate": round(negative / total * 100, 1) if total else 0,
        "blocking_incidents": blocking,
        "top_theme": top_theme,
    }


def backlog(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("theme", dropna=False).agg(
        volume=("text", "count"),
        negative_rate=("sentiment", lambda s: round((s == "Négatif").mean() * 100, 1)),
        blocking_incidents=("is_blocking", "sum"),
        avg_priority_score=("priority_score", "mean"),
        recommendation=("recommended_action", "first"),
    ).reset_index()
    grouped["avg_priority_score"] = grouped["avg_priority_score"].round(1)
    grouped["volume_share"] = (grouped["volume"] / max(grouped["volume"].sum(), 1) * 100).round(1)
    grouped["priority"] = grouped["avg_priority_score"].apply(lambda x: "P0" if x >= 70 else "P1" if x >= 55 else "P2" if x >= 40 else "P3")
    grouped["impact"] = grouped["priority"].map({"P0": "Critique", "P1": "Élevé", "P2": "Moyen", "P3": "À surveiller"})
    return grouped.sort_values(["priority", "avg_priority_score"], ascending=[True, False])


def executive_summary(df: pd.DataFrame) -> str:
    if df.empty:
        return "Aucune donnée analysée."
    b = backlog(df).iloc[0]
    return (
        f"Le sujet prioritaire est '{b['theme']}', représentant {b['volume_share']}% des verbatims. "
        f"Son niveau d’impact est {b['impact'].lower()} avec {int(b['blocking_incidents'])} incidents bloquants détectés. "
        f"Action recommandée : {b['recommendation']}"
    )
