import re
import pandas as pd


TAXONOMY = {
    "Livraison / Logistique": ["livraison", "retard", "colis", "transporteur", "endommagé", "reçu"],
    "Support client": ["support", "service client", "réponse", "attente", "agent", "contact"],
    "Remboursement / Facturation": ["remboursement", "facture", "paiement", "prélevé", "argent", "tarif"],
    "Produit / Qualité": ["produit", "qualité", "cassé", "défectueux", "bug", "fonctionne"],
    "Onboarding / Usage": ["onboarding", "activation", "connexion", "compte", "interface", "documentation"],
    "Démarches administratives": ["passeport", "visa", "rendez-vous", "dossier", "document", "administratif"],
    "Communication": ["information", "communication", "procédure", "clair", "mail", "appel"],
}


NEGATIVE_WORDS = [
    "problème", "retard", "lent", "impossible", "déçu", "mauvais",
    "bloqué", "erreur", "jamais", "attente", "plainte", "difficile",
    "confus", "cher", "cassé", "perdu"
]

BLOCKING_WORDS = [
    "impossible", "bloqué", "urgent", "jamais", "aucune réponse",
    "ne fonctionne pas", "perdu", "annulé", "refusé"
]


def clean_text(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def detect_theme(text: str):
    cleaned = clean_text(text)
    scores = {}

    for theme, keywords in TAXONOMY.items():
        score = sum(1 for keyword in keywords if keyword in cleaned)
        scores[theme] = score

    best_theme = max(scores, key=scores.get)
    best_score = scores[best_theme]

    if best_score == 0:
        return "Autre / Non classé", "", 0

    matched_keywords = [
        keyword for keyword in TAXONOMY[best_theme]
        if keyword in cleaned
    ]

    return best_theme, ", ".join(matched_keywords), best_score


def detect_sentiment(text: str) -> str:
    cleaned = clean_text(text)
    negative_score = sum(1 for word in NEGATIVE_WORDS if word in cleaned)

    if negative_score >= 2:
        return "Négatif"
    if negative_score == 1:
        return "Neutre"
    return "Positif"


def detect_blocking(text: str) -> bool:
    cleaned = clean_text(text)
    return any(word in cleaned for word in BLOCKING_WORDS)


def severity_score(sentiment: str, is_blocking: bool, theme_score: int) -> int:
    score = 1

    if sentiment == "Neutre":
        score += 1
    if sentiment == "Négatif":
        score += 2
    if is_blocking:
        score += 2
    if theme_score >= 2:
        score += 1

    return min(score, 5)


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "text" not in df.columns:
        raise ValueError("La colonne standardisée 'text' est absente.")

    themes = []
    keywords = []
    theme_scores = []
    sentiments = []
    blockings = []
    severities = []

    for text in df["text"]:
        theme, matched, theme_score = detect_theme(text)
        sentiment = detect_sentiment(text)
        blocking = detect_blocking(text)
        severity = severity_score(sentiment, blocking, theme_score)

        themes.append(theme)
        keywords.append(matched)
        theme_scores.append(theme_score)
        sentiments.append(sentiment)
        blockings.append(blocking)
        severities.append(severity)

    df["theme"] = themes
    df["matched_keywords"] = keywords
    df["theme_score"] = theme_scores
    df["sentiment"] = sentiments
    df["is_blocking"] = blockings
    df["severity_score"] = severities

    return df