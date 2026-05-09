TAXONOMIES = {
    "ecommerce": {
        "Livraison": ["livraison", "retard", "colis", "transporteur", "expédition", "arrivé", "arrivée"],
        "Remboursement": ["remboursement", "remboursé", "argent", "retour", "avoir"],
        "Support client": ["support", "service client", "réponse", "contact", "conseiller", "agent"],
        "Qualité produit": ["cassé", "défectueux", "qualité", "abimé", "endommagé", "taille"],
        "Paiement": ["paiement", "carte", "facture", "transaction", "erreur paiement"],
    },
    "saas": {
        "Onboarding": ["onboarding", "activation", "démarrage", "configuration", "paramétrage"],
        "Bugs": ["bug", "erreur", "crash", "bloqué", "lent", "latence"],
        "UX complexe": ["complexe", "difficile", "interface", "navigation", "ergonomie"],
        "Documentation": ["documentation", "guide", "tutoriel", "aide", "explication"],
        "Support": ["support", "ticket", "réponse", "assistance", "contact"],
    },
    "embassy": {
        "Délais administratifs": ["délai", "attente", "retard", "traitement", "long", "semaine"],
        "Rendez-vous": ["rendez-vous", "rdv", "créneau", "disponibilité", "planning"],
        "Communication": ["réponse", "email", "appel", "communication", "information", "joindre"],
        "Procédures": ["procédure", "document", "formulaire", "dossier", "pièce", "justificatif"],
        "Accueil": ["accueil", "agent", "guichet", "orientation", "amabilité"],
    },
    "generic": {
        "Support": ["support", "service", "réponse", "contact", "aide"],
        "Délais": ["délai", "retard", "attente", "long"],
        "Qualité": ["qualité", "problème", "défectueux", "erreur"],
        "Prix / Facturation": ["prix", "facture", "paiement", "coût", "cher"],
        "Expérience": ["expérience", "simple", "difficile", "complexe", "satisfait"],
    },
}

NEGATIVE_WORDS = ["problème", "retard", "lent", "déçu", "déçue", "impossible", "mauvais", "bug", "erreur", "difficile", "long", "bloqué", "cassé", "inefficace", "manque", "jamais"]
POSITIVE_WORDS = ["satisfait", "rapide", "excellent", "merci", "simple", "clair", "efficace", "parfait", "bien", "utile"]
BLOCKING_WORDS = ["impossible", "bloqué", "bloquée", "urgent", "critique", "jamais", "aucune réponse", "ne fonctionne pas", "annuler", "résilier"]
