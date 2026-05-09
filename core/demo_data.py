from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

DEMOS = {
    "ecommerce": {
        "name": "RetailCX Intelligence",
        "subtitle": "E-commerce, livraison, SAV et remboursement",
        "story": "La majorité des frustrations clients ne provient pas des produits mais de l’expérience post-achat.",
        "path": ROOT / "data" / "demo" / "ecommerce" / "feedbacks.csv",
    },
    "saas": {
        "name": "SaaS Product Signals",
        "subtitle": "Onboarding, activation, bugs et support produit",
        "story": "Le churn utilisateur commence souvent avant même l’activation complète du produit.",
        "path": ROOT / "data" / "demo" / "saas" / "feedbacks.csv",
    },
    "embassy": {
        "name": "Consular Experience Intelligence",
        "subtitle": "Ambassade du Congo, demandes consulaires et expérience citoyenne",
        "story": "Les frustrations administratives détruisent la confiance citoyenne avant même la qualité du service rendu.",
        "path": ROOT / "data" / "demo" / "embassy" / "feedbacks.csv",
    },
}


def load_demo(key):
    return pd.read_csv(DEMOS[key]["path"])
