from __future__ import annotations
import pandas as pd


def enrich_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["severity_score"] = df["severity_base"] + df["is_blocking"].astype(int) * 2 + (df["sentiment"] == "Négatif").astype(int)
    df["severity_score"] = df["severity_score"].clip(1, 10)
    counts = df["theme"].value_counts(normalize=True).to_dict()
    df["frequency_rate"] = df["theme"].map(counts).fillna(0)
    df["priority_score"] = (df["frequency_rate"] * 40) + (df["severity_score"] * 6) + (df["is_blocking"].astype(int) * 15)
    df["priority_score"] = df["priority_score"].round(1)
    return df


def priority_label(score: float) -> str:
    if score >= 70:
        return "P0"
    if score >= 55:
        return "P1"
    if score >= 40:
        return "P2"
    return "P3"
