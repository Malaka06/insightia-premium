from pathlib import Path
import random
import pandas as pd


ROOT = Path(__file__).resolve().parent
DEMO_DIR = ROOT / "data" / "demo"

random.seed(42)


DEMOS = {
    "ecommerce": {
        "n": 8500,
        "segments": ["Nouveau client", "Client régulier", "Client premium", "Client entreprise"],
        "regions": ["Île-de-France", "Hauts-de-France", "Auvergne-Rhône-Alpes", "Belgique", "Suisse"],
        "channels": ["Avis site", "Email SAV", "Chat client", "Trustpilot", "Application mobile"],
        "products": ["Livraison standard", "Livraison express", "Retour produit", "Commande marketplace", "Abonnement premium"],
        "journeys": ["Achat", "Livraison", "Retour", "Remboursement", "Support après-vente"],
        "issues": [
            {
                "theme": "Livraison / Logistique",
                "weight": 30,
                "subthemes": [
                    "retard livraison express",
                    "suivi colis incohérent",
                    "colis marqué livré mais non reçu",
                    "transporteur injoignable",
                    "colis endommagé",
                ],
                "comments": [
                    "J’ai payé une livraison express pour recevoir ma commande avant un déplacement, mais le colis est arrivé avec plusieurs jours de retard.",
                    "Le colis a été reporté trois fois sans information claire. J’ai dû contacter le service client moi-même pour comprendre où était ma commande.",
                    "Mon colis est arrivé abîmé et l’emballage était ouvert. J’ai perdu confiance dans la capacité de la marque à gérer correctement une commande importante.",
                    "Le suivi colis changeait tous les jours entre en préparation, expédié et livré. Impossible de savoir où était réellement la commande.",
                ],
                "impact": "perte de confiance post-achat",
            },
            {
                "theme": "Remboursement / Facturation",
                "weight": 22,
                "subthemes": [
                    "remboursement trop lent",
                    "montant incorrect",
                    "double prélèvement",
                    "facture incompréhensible",
                    "avoir non reçu",
                ],
                "comments": [
                    "Le remboursement devait être effectué sous quelques jours, mais après deux semaines je n’ai toujours rien reçu.",
                    "J’ai été prélevé deux fois pour la même commande. La facture ne permet pas de comprendre ce qui a été payé ou remboursé.",
                    "Le montant remboursé ne correspond pas au montant validé lors du retour.",
                    "J’ai reçu un avoir au lieu d’un remboursement alors que j’avais demandé un remboursement bancaire.",
                ],
                "impact": "friction financière et perte de crédibilité",
            },
            {
                "theme": "Support client",
                "weight": 20,
                "subthemes": [
                    "réponses automatiques",
                    "relances multiples",
                    "absence de suivi",
                    "réponses contradictoires",
                    "délai de réponse long",
                ],
                "comments": [
                    "J’ai contacté le support trois fois et j’ai reçu trois réponses différentes.",
                    "Le service client répond avec des messages automatiques qui ne traitent pas mon problème.",
                    "J’ai ouvert une demande urgente mais je n’ai reçu aucune réponse utile pendant plusieurs jours.",
                    "L’agent était poli, mais il n’avait pas la capacité de résoudre le problème.",
                ],
                "impact": "augmentation des relances et baisse satisfaction",
            },
            {
                "theme": "Produit / Qualité",
                "weight": 16,
                "subthemes": [
                    "produit défectueux",
                    "produit incomplet",
                    "qualité inférieure aux photos",
                    "erreur de taille",
                    "emballage insuffisant",
                ],
                "comments": [
                    "Le produit reçu ne correspond pas aux photos du site.",
                    "Il manque une pièce essentielle dans le colis, donc je ne peux pas utiliser le produit.",
                    "Le produit fonctionne, mais l’emballage était insuffisant et plusieurs éléments étaient rayés à l’arrivée.",
                    "J’ai reçu une mauvaise taille malgré une commande correctement validée.",
                ],
                "impact": "dégradation de la promesse produit",
            },
            {
                "theme": "Communication",
                "weight": 12,
                "subthemes": [
                    "emails peu clairs",
                    "informations contradictoires",
                    "manque de transparence",
                    "statut commande imprécis",
                    "absence de notification proactive",
                ],
                "comments": [
                    "Les emails de suivi ne sont pas clairs. Je ne sais pas si ma commande est en préparation, expédiée ou bloquée.",
                    "Le site indique une chose, le transporteur une autre, et le support encore une autre.",
                    "Je n’ai reçu aucune notification proactive alors que ma commande était en retard.",
                    "Les informations sur les délais sont trop générales.",
                ],
                "impact": "manque de visibilité client",
            },
        ],
    },

    "saas": {
        "n": 6800,
        "segments": ["PME", "Startup", "Grand compte", "Équipe produit", "Équipe support"],
        "regions": ["France", "Belgique", "Suisse", "Canada", "Afrique francophone"],
        "channels": ["Ticket support", "Enquête NPS", "Chat produit", "Email client", "Feedback onboarding"],
        "products": ["Dashboard analytics", "Module onboarding", "API", "Export reporting", "Gestion utilisateurs"],
        "journeys": ["Activation", "Configuration", "Usage quotidien", "Support", "Renouvellement"],
        "issues": [
            {
                "theme": "Onboarding / Usage",
                "weight": 30,
                "subthemes": [
                    "activation trop longue",
                    "parcours confus",
                    "manque d’accompagnement",
                    "configuration complexe",
                    "première valeur trop tardive",
                ],
                "comments": [
                    "L’onboarding est trop long. Notre équipe n’a pas compris quelles étapes étaient indispensables.",
                    "La configuration initiale demande trop d’allers-retours avec le support.",
                    "Les nouveaux utilisateurs se perdent dans l’interface dès la première connexion.",
                    "Nous ne savons pas quoi faire après la création du compte.",
                ],
                "impact": "risque de non-adoption et churn précoce",
            },
            {
                "theme": "Produit / Qualité",
                "weight": 25,
                "subthemes": [
                    "bug bloquant",
                    "export instable",
                    "lenteur dashboard",
                    "métriques incohérentes",
                    "perte de données",
                ],
                "comments": [
                    "Un bug bloque l’export des données au moment où nous devons préparer notre reporting mensuel.",
                    "Le tableau de bord met trop de temps à charger dès que le volume de données augmente.",
                    "Certaines métriques changent sans explication entre deux connexions.",
                    "L’API retourne parfois des erreurs sans message clair.",
                ],
                "impact": "perte de confiance dans la donnée produit",
            },
            {
                "theme": "Support client",
                "weight": 18,
                "subthemes": [
                    "support lent",
                    "réponse générique",
                    "ticket sans suivi",
                    "escalade difficile",
                    "absence de délai",
                ],
                "comments": [
                    "Le support répond trop tard pour un incident bloquant en production.",
                    "Nous avons reçu une réponse générique alors que le ticket contenait des captures et des logs détaillés.",
                    "Le suivi du ticket manque de clarté. Personne ne donne de délai.",
                    "L’escalade vers une personne technique prend trop de temps.",
                ],
                "impact": "risque contractuel et insatisfaction compte clé",
            },
            {
                "theme": "Communication",
                "weight": 15,
                "subthemes": [
                    "release note absente",
                    "documentation confuse",
                    "changement non annoncé",
                    "manque de roadmap",
                    "statut incident peu visible",
                ],
                "comments": [
                    "Les changements de fonctionnalités ne sont pas suffisamment annoncés.",
                    "La documentation ne montre pas clairement les impacts des nouveaux paramètres.",
                    "Lorsqu’un incident est en cours, le statut n’est pas assez visible.",
                    "La roadmap manque de clarté.",
                ],
                "impact": "manque de prévisibilité pour les clients B2B",
            },
            {
                "theme": "Facturation / Pricing",
                "weight": 12,
                "subthemes": [
                    "tarification peu claire",
                    "options avancées mal expliquées",
                    "facture détaillée insuffisante",
                    "coût utilisateur imprévisible",
                    "renouvellement mal anticipé",
                ],
                "comments": [
                    "La tarification est difficile à comprendre pour les options avancées.",
                    "La facture mensuelle ne détaille pas assez les modules activés.",
                    "Le coût par utilisateur devient difficile à anticiper quand plusieurs équipes rejoignent la plateforme.",
                    "Le renouvellement annuel arrive sans synthèse claire de l’usage réel.",
                ],
                "impact": "frein au renouvellement et à l’expansion",
            },
        ],
    },

    "embassy": {
        "n": 9200,
        "segments": ["Étudiant", "Famille", "Professionnel", "Urgence voyage", "Diaspora"],
        "regions": ["France", "Belgique", "Luxembourg", "Suisse", "Pays-Bas"],
        "channels": ["Email consulaire", "Formulaire de contact", "Accueil physique", "Téléphone", "Avis citoyen"],
        "products": ["Passeport", "Visa", "Acte consulaire", "Légalisation", "Rendez-vous"],
        "journeys": ["Prise de rendez-vous", "Dépôt dossier", "Suivi dossier", "Paiement", "Retrait document"],
        "issues": [
            {
                "theme": "Démarches administratives",
                "weight": 36,
                "subthemes": [
                    "rendez-vous indisponible",
                    "procédure passeport confuse",
                    "dossier sans suivi",
                    "délai traitement long",
                    "documents demandés contradictoires",
                ],
                "comments": [
                    "Je n’arrive pas à obtenir un rendez-vous pour le renouvellement de mon passeport.",
                    "Mon dossier est complet, mais je n’ai reçu aucun suivi depuis plusieurs semaines.",
                    "La procédure indiquée sur le site ne correspond pas aux documents demandés sur place.",
                    "Le délai de traitement bloque mon voyage alors que la situation est urgente.",
                ],
                "impact": "perte de confiance citoyenne et saturation des demandes",
            },
            {
                "theme": "Communication",
                "weight": 28,
                "subthemes": [
                    "emails sans réponse",
                    "information visa confuse",
                    "téléphone injoignable",
                    "procédure peu lisible",
                    "absence de notification",
                ],
                "comments": [
                    "J’ai envoyé plusieurs emails mais je n’ai pas reçu de réponse claire.",
                    "Les informations sur le visa sont difficiles à comprendre et changent selon l’interlocuteur.",
                    "Le téléphone sonne longtemps sans réponse.",
                    "Aucune notification n’est envoyée pour expliquer l’avancement du dossier.",
                ],
                "impact": "augmentation des relances et incompréhension des procédures",
            },
            {
                "theme": "Accueil / Support usager",
                "weight": 18,
                "subthemes": [
                    "orientation insuffisante",
                    "répétition dossier",
                    "absence de délai",
                    "manque de suivi personnalisé",
                    "expérience stressante",
                ],
                "comments": [
                    "L’accueil est poli, mais personne ne peut me donner un délai précis.",
                    "Je dois répéter ma situation à chaque contact.",
                    "On m’a demandé de revenir avec un document qui n’était pas mentionné avant.",
                    "La situation est stressante car mon dossier concerne une urgence familiale.",
                ],
                "impact": "expérience usager dégradée",
            },
            {
                "theme": "Paiement / Frais consulaires",
                "weight": 10,
                "subthemes": [
                    "frais peu expliqués",
                    "paiement supplémentaire",
                    "reçu manquant",
                    "tarif incompris",
                    "mode paiement limité",
                ],
                "comments": [
                    "Les frais consulaires ne sont pas expliqués clairement avant le dépôt du dossier.",
                    "Je ne comprends pas pourquoi un paiement supplémentaire est demandé.",
                    "Le reçu n’indique pas clairement à quelle démarche correspond le paiement.",
                    "Les modes de paiement disponibles ne sont pas assez pratiques.",
                ],
                "impact": "friction administrative et manque de transparence",
            },
            {
                "theme": "Digitalisation / Suivi en ligne",
                "weight": 8,
                "subthemes": [
                    "absence espace usager",
                    "suivi dossier impossible",
                    "formulaire peu ergonomique",
                    "documents non téléversables",
                    "manque de confirmation automatique",
                ],
                "comments": [
                    "Un espace en ligne pour suivre l’état du dossier éviterait beaucoup de relances.",
                    "Après avoir rempli le formulaire, je ne reçois pas de confirmation claire avec un numéro de suivi.",
                    "Il serait utile de pouvoir téléverser les documents avant le rendez-vous.",
                    "Le formulaire de contact est trop limité pour expliquer correctement les situations urgentes.",
                ],
                "impact": "opportunité de modernisation du service public",
            },
        ],
    },
}


POSITIVE_COMMENTS = [
    "Le service a été rapide, clair et la personne en charge m’a donné une réponse utile.",
    "L’expérience s’est bien passée. Les informations étaient compréhensibles et le suivi était correct.",
    "Le problème a été résolu rapidement après mon contact avec le support.",
    "J’ai apprécié la clarté des informations et le professionnalisme de l’équipe.",
    "merci au support cette fois, problème réglé rapidement",
    "super expérience, rien à signaler",
    "réponse rapide et claire",
]

NEUTRAL_COMMENTS = [
    "Le service fonctionne, mais certaines étapes pourraient être mieux expliquées.",
    "L’expérience est correcte, mais il manque un suivi plus visible.",
    "Je n’ai pas rencontré de blocage majeur, mais la communication pourrait être améliorée.",
    "La procédure est faisable, mais elle demande beaucoup d’attention pour éviter une erreur.",
    "bof, ça marche mais ce n’est pas très clair",
    "pas bloqué mais pas fluide non plus",
    "à revoir, surtout les explications",
]

SHORT_COMMENTS = [
    "toujours rien reçu",
    "support impossible",
    "très déçu",
    "ça bug encore",
    "aucune réponse",
    "franchement abusé",
    "super cette fois",
    "nul",
    "bof",
    "service lent",
    "bloqué depuis hier",
    "merci au support",
    "jattend toujours",
    "impossible de suivre le dossier",
    "ça devient pénible",
    "retard encore",
    "personne répond",
    "très long",
    "vraiment compliqué",
    "je comprends pas",
    "service catastrophique",
    "pas normal",
    "aucune visibilité",
    "toujours le même problème",
]

MESSY_COMMENTS = [
    "jattend depuis 2 semaine",
    "personne repond",
    "toujours aucun remboursement",
    "je comprend pas le suivi",
    "ca marche pas",
    "bloqué encore",
    "aucun retour depuis des jours",
    "commande jamais recu",
    "toujours rien...",
    "tjr aucun suivi",
    "trop lent franchement",
    "impossible de payer",
    "support repond a coté",
    "jai deja relancé 3 fois",
    "on m’a dit d’attendre mais rien bouge",
    "c’est pas clair du tout",
]

CONSEQUENCES = [
    "Cela m’a obligé à relancer plusieurs fois.",
    "Cela a créé une perte de confiance.",
    "Cela a retardé une décision importante.",
    "Cela a augmenté le stress autour de la démarche.",
    "Cela donne l’impression que le suivi n’est pas maîtrisé.",
    "Cela peut pousser un client à ne pas revenir.",
]

URGENCY_WORDS = [
    "urgent",
    "bloque",
    "bloquant",
    "impossible",
    "aucun",
    "plusieurs semaines",
    "retard",
    "perte de confiance",
    "production",
]


def choose_issue(issues):
    return random.choices(
        issues,
        weights=[issue["weight"] for issue in issues],
        k=1,
    )[0]


def score_from_comment(comment, sentiment):
    text = comment.lower()

    if sentiment == "positive":
        return random.choice([4, 5])

    if sentiment == "neutral":
        return random.choice([3, 4])

    if any(word in text for word in ["urgent", "bloque", "bloquant", "impossible", "aucun", "plusieurs semaines"]):
        return random.choices([1, 2], weights=[65, 35], k=1)[0]

    return random.choices([1, 2, 3], weights=[35, 45, 20], k=1)[0]


def urgency_from_comment(comment):
    text = comment.lower()
    count = sum(1 for word in URGENCY_WORDS if word in text)

    if count >= 3:
        return "Critique"
    if count >= 2:
        return "Élevée"
    if count == 1:
        return "Modérée"
    return "Faible"


def is_blocking(comment):
    text = comment.lower()
    return any(
        word in text
        for word in [
            "bloque",
            "bloquant",
            "impossible",
            "urgent",
            "aucun moyen",
            "production",
            "aucune réponse",
            "aucun retour",
            "jamais recu",
            "jamais reçu",
        ]
    )


def enrich_comment(base, segment, region, product, journey):
    additions = [
        f" Le cas concerne le segment {segment.lower()}, sur le parcours {journey.lower()}, avec un impact direct sur {product.lower()}.",
        f" Cette situation est remontée depuis {region} et touche surtout le parcours {journey.lower()}.",
        f" Pour un profil {segment.lower()}, ce niveau de friction réduit fortement la confiance dans le service.",
        f" Le problème n’est pas isolé : il génère des relances, de l’incertitude et une perception de manque de maîtrise.",
        f" {random.choice(CONSEQUENCES)}",
    ]

    return base + random.choice(additions)


def build_comment(sentiment, issue, segment, region, product, journey):
    if sentiment == "positive":
        return random.choice(POSITIVE_COMMENTS)

    if sentiment == "neutral":
        return random.choices(
            [
                random.choice(NEUTRAL_COMMENTS),
                random.choice(SHORT_COMMENTS),
            ],
            weights=[80, 20],
            k=1,
        )[0]

    comment = random.choices(
        [
            random.choice(issue["comments"]),
            random.choice(SHORT_COMMENTS),
            random.choice(MESSY_COMMENTS),
        ],
        weights=[70, 20, 10],
        k=1,
    )[0]

    if len(comment) > 40:
        comment = enrich_comment(
            comment,
            segment,
            region,
            product,
            journey,
        )

    return comment


def generate_dataset(name):
    config = DEMOS[name]
    rows = []

    for i in range(1, config["n"] + 1):
        segment = random.choice(config["segments"])
        region = random.choice(config["regions"])
        channel = random.choice(config["channels"])
        product = random.choice(config["products"])
        journey = random.choice(config["journeys"])

        base_date = pd.Timestamp("2025-01-01")

        if name == "ecommerce":
            day = random.choices(
                range(0, 420),
                weights=[3 if 300 <= d <= 360 else 1 for d in range(0, 420)],
                k=1,
            )[0]
        elif name == "saas":
            day = random.choices(
                range(0, 420),
                weights=[3 if 120 <= d <= 180 else 1 for d in range(0, 420)],
                k=1,
            )[0]
        else:
            day = random.choices(
                range(0, 420),
                weights=[3 if 180 <= d <= 260 else 1 for d in range(0, 420)],
                k=1,
            )[0]

        date = base_date + pd.Timedelta(days=day)

        sentiment = random.choices(
            ["negative", "neutral", "positive"],
            weights=[72, 18, 10],
            k=1,
        )[0]

        if sentiment == "positive":
            theme = "Expérience positive"
            subtheme = "service satisfaisant"
            irritant = "aucun irritant majeur"
            impact = "satisfaction et confiance"
            comment = build_comment(sentiment, None, segment, region, product, journey)

        elif sentiment == "neutral":
            theme = "Communication"
            subtheme = "amélioration souhaitée"
            irritant = "manque de clarté partiel"
            impact = "friction légère"
            comment = build_comment(sentiment, None, segment, region, product, journey)

        else:
            issue = choose_issue(config["issues"])
            theme = issue["theme"]
            subtheme = random.choice(issue["subthemes"])
            irritant = subtheme
            impact = issue["impact"]
            comment = build_comment(sentiment, issue, segment, region, product, journey)

        score = score_from_comment(comment, sentiment)
        urgency = urgency_from_comment(comment)
        blocking = is_blocking(comment)

        rows.append(
            {
                "feedback_id": f"{name.upper()}-{i:06d}",
                "date": date.date().isoformat(),
                "canal": channel,
                "segment_client": segment,
                "region": region,
                "produit_service": product,
                "parcours_client": journey,
                "score": score,
                "sentiment_attendu": sentiment,
                "theme_attendu": theme,
                "sous_theme": subtheme,
                "irritant": irritant,
                "niveau_urgence": urgency,
                "impact_business": impact,
                "est_bloquant": blocking,
                "commentaire": comment,
            }
        )

    df = pd.DataFrame(rows)

    output_dir = DEMO_DIR / name
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_dir / "feedbacks.csv", index=False, encoding="utf-8-sig")

    print(f"{name}: {len(df)} lignes générées")


if __name__ == "__main__":
    generate_dataset("ecommerce")
    generate_dataset("saas")
    generate_dataset("embassy")
    print("Données démo premium générées avec succès.")