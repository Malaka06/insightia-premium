from pathlib import Path
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]

DEMO_PATHS = {
    "ecommerce": ROOT_DIR / "data" / "demo" / "ecommerce" / "feedbacks.csv",
    "saas": ROOT_DIR / "data" / "demo" / "saas" / "feedbacks.csv",
    "embassy": ROOT_DIR / "data" / "demo" / "embassy" / "feedbacks.csv",
}


def read_csv_robust(file):
    encodings = ["utf-8-sig", "utf-8", "latin1", "cp1252"]

    for encoding in encodings:
        try:
            return pd.read_csv(file, encoding=encoding)
        except Exception:
            if hasattr(file, "seek"):
                file.seek(0)

    raise ValueError("Impossible de lire le fichier CSV.")


def load_demo(demo_name: str):
    if demo_name not in DEMO_PATHS:
        raise ValueError(f"Démo inconnue : {demo_name}")

    path = DEMO_PATHS[demo_name]

    if not path.exists():
        raise FileNotFoundError(f"Fichier démo introuvable : {path}")

    return read_csv_robust(path)


def standardize_columns(df: pd.DataFrame):
    df = df.copy()

    if "commentaire" in df.columns:
        df["text"] = df["commentaire"].astype(str)
    elif "feedback" in df.columns:
        df["text"] = df["feedback"].astype(str)
    elif "message" in df.columns:
        df["text"] = df["message"].astype(str)
    else:
        raise ValueError("Aucune colonne texte trouvée : commentaire, feedback ou message.")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["channel"] = df["canal"].astype(str) if "canal" in df.columns else "Non renseigné"
    df["score"] = pd.to_numeric(df["score"], errors="coerce") if "score" in df.columns else None

    return df