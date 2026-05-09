import re
import unicodedata
import pandas as pd
from core.taxonomy import TAXONOMIES, NEGATIVE_WORDS, POSITIVE_WORDS, BLOCKING_WORDS


def normalize_text(text):
    text = str(text).lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("utf-8")
    text = re.sub(r"[^a-z0-9\s'-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def count_matches(text, words):
    clean = normalize_text(text)
    return sum(1 for word in words if normalize_text(word) in clean)


def classify_theme(text, demo_key="generic"):
    taxonomy = TAXONOMIES.get(demo_key, TAXONOMIES["generic"])
    scores = {theme: count_matches(text, words) for theme, words in taxonomy.items()}
    best_theme = max(scores, key=scores.get)
    best_score = scores[best_theme]
    matched = [w for w in taxonomy[best_theme] if normalize_text(w) in normalize_text(text)]
    if best_score == 0:
        return "Autre / Non classé", 0, ""
    return best_theme, best_score, ", ".join(matched[:6])


def sentiment_label(text):
    neg = count_matches(text, NEGATIVE_WORDS)
    pos = count_matches(text, POSITIVE_WORDS)
    if neg > pos:
        return "Négatif"
    if pos > neg:
        return "Positif"
    return "Neutre"


def severity_score(text, score=None):
    neg = count_matches(text, NEGATIVE_WORDS)
    block = count_matches(text, BLOCKING_WORDS)
    base = min(5, 1 + neg + block * 2)
    if pd.notna(score):
        try:
            s = float(score)
            if s <= 2:
                base += 2
            elif s <= 3:
                base += 1
        except Exception:
            pass
    return min(5, base)


def run_pipeline(df, demo_key="generic"):
    data = df.copy()
    data["clean_text"] = data["text"].apply(normalize_text)
    classified = data["text"].apply(lambda x: classify_theme(x, demo_key))
    data["theme"] = classified.apply(lambda x: x[0])
    data["theme_score"] = classified.apply(lambda x: x[1])
    data["matched_keywords"] = classified.apply(lambda x: x[2])
    data["sentiment"] = data["text"].apply(sentiment_label)
    data["is_blocking"] = data["text"].apply(lambda x: count_matches(x, BLOCKING_WORDS) > 0)
    data["severity_score"] = data.apply(lambda r: severity_score(r["text"], r.get("score")), axis=1)
    return data
