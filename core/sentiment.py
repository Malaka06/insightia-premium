from __future__ import annotations
from core.preprocessing import normalize_text

NEGATIVE = ["retard", "lent", "attente", "impossible", "bloque", "bug", "erreur", "mauvais", "decu", "jamais", "probleme", "complique", "confus", "cass", "abime", "cher", "injoignable"]
POSITIVE = ["excellent", "merci", "rapide", "clair", "satisfait", "simple", "efficace", "parfait", "utile", "bien"]
BLOCKING = ["impossible", "bloque", "jamais", "urgent", "panne", "crash", "aucun", "injoignable"]


def analyze_sentiment(text: str) -> dict:
    normalized = normalize_text(text)
    neg = sum(1 for w in NEGATIVE if w in normalized)
    pos = sum(1 for w in POSITIVE if w in normalized)
    blocking = any(w in normalized for w in BLOCKING)

    if neg > pos:
        sentiment = "Négatif"
        sentiment_score = -min(1.0, neg / 4)
    elif pos > neg:
        sentiment = "Positif"
        sentiment_score = min(1.0, pos / 4)
    else:
        sentiment = "Neutre"
        sentiment_score = 0

    return {
        "sentiment": sentiment,
        "sentiment_score": round(sentiment_score, 2),
        "is_blocking": blocking,
    }
