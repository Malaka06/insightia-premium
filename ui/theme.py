import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(124,58,237,0.18), transparent 28%),
                radial-gradient(circle at top right, rgba(30,64,175,0.12), transparent 26%),
                linear-gradient(135deg, #050814 0%, #070B14 48%, #020617 100%);
            color: #F8FAFC;
        }

        .block-container {
            max-width: 1420px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        .hero-wrapper {
            display: grid;
            grid-template-columns: 1.55fr 0.75fr;
            gap: 34px;
            align-items: stretch;
            padding: 38px;
            border-radius: 36px;
            background:
                linear-gradient(135deg, rgba(124,58,237,0.24), rgba(15,23,42,0.82)),
                radial-gradient(circle at top right, rgba(167,139,250,0.22), transparent 38%);
            border: 1px solid rgba(148,163,184,0.18);
            box-shadow: 0 36px 110px rgba(0,0,0,0.36);
            margin-bottom: 28px;
        }

        .hero-left {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .hero-badge, .section-kicker, .card-label, .panel-label, .summary-label,
        .empty-kicker, .filter-title, .friction-kicker {
            text-transform: uppercase;
        }

        .hero-badge {
            width: fit-content;
            padding: 10px 16px;
            border-radius: 999px;
            background: rgba(124,58,237,0.22);
            border: 1px solid rgba(167,139,250,0.40);
            color: #DDD6FE;
            font-size: 12px;
            font-weight: 900;
            letter-spacing: 0.09em;
            margin-bottom: 28px;
        }

        .hero-title {
            max-width: 980px;
            font-size: 68px;
            line-height: 1.02;
            letter-spacing: -0.065em;
            color: #FFFFFF;
            font-weight: 950;
            margin-bottom: 24px;
        }

        .hero-subtitle {
            max-width: 920px;
            color: #D1D5DB;
            font-size: 21px;
            line-height: 1.75;
            margin-bottom: 26px;
        }

        .hero-proof {
            width: fit-content;
            color: #C4B5FD;
            font-size: 15px;
            font-weight: 850;
            padding: 13px 16px;
            border-radius: 18px;
            border: 1px solid rgba(167,139,250,0.26);
            background: rgba(15,23,42,0.60);
        }

        .hero-panel, .recommendation-panel {
            padding: 28px;
            border-radius: 30px;
            background:
                linear-gradient(180deg, rgba(15,23,42,0.95), rgba(2,6,23,0.92));
            border: 1px solid rgba(167,139,250,0.24);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
            min-height: 360px;
        }

        .panel-label {
            color: #A78BFA;
            font-size: 12px;
            letter-spacing: 0.12em;
            font-weight: 900;
            margin-bottom: 20px;
        }

        .panel-value {
            font-size: 72px;
            line-height: 0.95;
            color: #FFFFFF;
            font-weight: 950;
            letter-spacing: -0.08em;
            margin-bottom: 18px;
        }

        .panel-title {
            font-size: 24px;
            line-height: 1.2;
            color: #FFFFFF;
            font-weight: 900;
            letter-spacing: -0.04em;
            margin-bottom: 14px;
        }

        .panel-text {
            color: #CBD5E1;
            font-size: 15px;
            line-height: 1.7;
        }

        .panel-divider {
            height: 1px;
            background: rgba(148,163,184,0.16);
            margin: 22px 0;
        }

        .panel-row {
            display: flex;
            justify-content: space-between;
            gap: 18px;
            padding: 10px 0;
            border-bottom: 1px solid rgba(148,163,184,0.08);
            color: #CBD5E1;
            font-size: 14px;
        }

        .panel-row strong {
            color: #FFFFFF;
            font-weight: 850;
            text-align: right;
        }

        .topnav {
            padding: 8px;
            border-radius: 22px;
            background: rgba(15,23,42,0.56);
            border: 1px solid rgba(148,163,184,0.12);
            margin-bottom: 26px;
        }

        div.stButton > button {
            min-height: 50px;
            border-radius: 16px;
            background: rgba(15,23,42,0.72);
            border: 1px solid rgba(148,163,184,0.18);
            color: #F8FAFC;
            font-size: 15px;
            font-weight: 800;
            transition: all 0.18s ease;
        }

        div.stButton > button:hover {
            border-color: rgba(167,139,250,0.58);
            background: rgba(124,58,237,0.22);
            color: #FFFFFF;
            transform: translateY(-1px);
        }

        .section-header {
            margin-bottom: 34px;
        }

        .section-header.compact {
            margin-bottom: 24px;
        }

        .section-kicker {
            color: #A78BFA;
            font-weight: 950;
            letter-spacing: 0.12em;
            font-size: 12px;
            margin-bottom: 12px;
        }

        .section-title {
            font-size: 50px;
            line-height: 1.05;
            letter-spacing: -0.055em;
            color: #FFFFFF;
            margin-bottom: 14px;
            font-weight: 950;
        }

        .section-description {
            max-width: 920px;
            font-size: 18px;
            line-height: 1.75;
            color: #CBD5E1;
        }

        .premium-card {
            min-height: 390px;
            height: 390px;
            padding: 34px;
            border-radius: 30px;
            background:
                linear-gradient(180deg, rgba(15,23,42,0.94), rgba(2,6,23,0.92));
            border: 1px solid rgba(148,163,184,0.16);
            box-shadow: 0 30px 80px rgba(0,0,0,0.28);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
        }

        .premium-card:hover {
            border-color: rgba(167,139,250,0.45);
            transform: translateY(-2px);
            transition: all 0.2s ease;
        }

        .card-label {
            color: #A78BFA;
            font-size: 12px;
            font-weight: 950;
            letter-spacing: 0.12em;
            margin-bottom: 22px;
        }

        .card-title {
            color: #FFFFFF;
            font-size: 40px;
            line-height: 1.05;
            letter-spacing: -0.055em;
            font-weight: 950;
            margin-bottom: 20px;
        }

        .card-subtitle {
            color: #CBD5E1;
            font-size: 17px;
            line-height: 1.65;
        }

        .card-story {
            color: #F8FAFC;
            font-size: 18px;
            line-height: 1.7;
            font-weight: 750;
            margin-top: 24px;
        }

        .insight-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 22px;
        }

        .insight-card {
            min-height: 230px;
            padding: 28px;
            border-radius: 28px;
            background:
                linear-gradient(180deg, rgba(15,23,42,0.88), rgba(2,6,23,0.90));
            border: 1px solid rgba(148,163,184,0.14);
            box-shadow: 0 22px 70px rgba(0,0,0,0.22);
        }

        .insight-badge {
            display: inline-block;
            padding: 8px 11px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 950;
            letter-spacing: 0.08em;
            margin-bottom: 20px;
        }

        .insight-badge.risk {
            color: #FECACA;
            background: rgba(239,68,68,0.14);
            border: 1px solid rgba(248,113,113,0.28);
        }

        .insight-badge.signal {
            color: #DDD6FE;
            background: rgba(124,58,237,0.16);
            border: 1px solid rgba(167,139,250,0.28);
        }

        .insight-badge.action {
            color: #BFDBFE;
            background: rgba(37,99,235,0.15);
            border: 1px solid rgba(96,165,250,0.25);
        }

        .insight-title {
            color: #FFFFFF;
            font-size: 24px;
            line-height: 1.18;
            letter-spacing: -0.04em;
            font-weight: 950;
            margin-bottom: 14px;
        }

        .insight-text {
            color: #CBD5E1;
            font-size: 16px;
            line-height: 1.7;
        }

        .executive-summary {
            padding: 34px;
            border-radius: 30px;
            background:
                linear-gradient(135deg, rgba(124,58,237,0.18), rgba(15,23,42,0.88));
            border: 1px solid rgba(167,139,250,0.22);
            box-shadow: 0 28px 80px rgba(0,0,0,0.28);
            margin-bottom: 28px;
        }

        .summary-label {
            color: #A78BFA;
            font-size: 12px;
            font-weight: 950;
            letter-spacing: 0.12em;
            margin-bottom: 14px;
        }

        .summary-title {
            font-size: 34px;
            line-height: 1.15;
            letter-spacing: -0.05em;
            font-weight: 950;
            color: #FFFFFF;
            margin-bottom: 16px;
        }

        .summary-title span {
            color: #C4B5FD;
        }

        .summary-text {
            color: #CBD5E1;
            font-size: 18px;
            line-height: 1.75;
            max-width: 1050px;
        }

        .decision-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 20px;
            margin-bottom: 42px;
        }

        .decision-card {
            padding: 26px;
            border-radius: 26px;
            background: rgba(15,23,42,0.82);
            border: 1px solid rgba(148,163,184,0.15);
            box-shadow: 0 18px 50px rgba(0,0,0,0.18);
        }

        .decision-label {
            color: #94A3B8;
            font-size: 13px;
            font-weight: 800;
            margin-bottom: 16px;
        }

        .decision-value {
            color: #FFFFFF;
            font-size: 42px;
            line-height: 1;
            font-weight: 950;
            letter-spacing: -0.06em;
            margin-bottom: 14px;
        }

        .decision-value.small {
            font-size: 27px;
            line-height: 1.15;
            letter-spacing: -0.04em;
        }

        .decision-note {
            color: #CBD5E1;
            font-size: 14px;
            line-height: 1.55;
        }

        .filter-panel {
            padding: 24px;
            border-radius: 24px;
            background: rgba(15,23,42,0.72);
            border: 1px solid rgba(148,163,184,0.12);
            margin-bottom: 24px;
        }

        .filter-title {
            color: #FFFFFF;
            font-size: 22px;
            font-weight: 900;
            letter-spacing: -0.04em;
            margin-bottom: 8px;
        }

        .filter-subtitle {
            color: #CBD5E1;
            font-size: 15px;
            line-height: 1.7;
        }

        .friction-card {
            padding: 30px;
            border-radius: 30px;
            background:
                linear-gradient(180deg, rgba(15,23,42,0.92), rgba(2,6,23,0.94));
            border: 1px solid rgba(148,163,184,0.14);
            box-shadow: 0 24px 70px rgba(0,0,0,0.22);
            margin-bottom: 22px;
        }

        .friction-header {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            align-items: flex-start;
            margin-bottom: 26px;
        }

        .friction-kicker {
            color: #A78BFA;
            font-size: 12px;
            font-weight: 950;
            letter-spacing: 0.12em;
            margin-bottom: 12px;
        }

        .friction-title {
            color: #FFFFFF;
            font-size: 34px;
            line-height: 1.08;
            letter-spacing: -0.05em;
            font-weight: 950;
        }

        .friction-score {
            padding: 14px 18px;
            border-radius: 16px;
            background: rgba(124,58,237,0.14);
            border: 1px solid rgba(167,139,250,0.24);
            color: #DDD6FE;
            font-size: 14px;
            font-weight: 850;
            white-space: nowrap;
        }

        .friction-body {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 18px;
            margin-bottom: 24px;
        }

        .friction-block {
            padding: 18px;
            border-radius: 18px;
            background: rgba(15,23,42,0.58);
            border: 1px solid rgba(148,163,184,0.08);
        }

        .friction-label {
            color: #94A3B8;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .friction-value {
            color: #FFFFFF;
            font-size: 18px;
            line-height: 1.5;
            font-weight: 750;
        }

        .friction-footer {
            display: flex;
            flex-wrap: wrap;
            gap: 18px;
            padding-top: 18px;
            border-top: 1px solid rgba(148,163,184,0.10);
            color: #CBD5E1;
            font-size: 14px;
        }

        .friction-footer strong {
            color: #FFFFFF;
        }

        .language-panel {
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
            padding: 28px;
            border-radius: 28px;
            background:
                linear-gradient(180deg, rgba(15,23,42,0.88), rgba(2,6,23,0.92));
            border: 1px solid rgba(148,163,184,0.12);
            margin-bottom: 12px;
        }

        .language-chip {
            padding: 12px 16px;
            border-radius: 999px;
            background: rgba(124,58,237,0.14);
            border: 1px solid rgba(167,139,250,0.22);
            color: #E9D5FF;
            font-size: 14px;
            font-weight: 750;
        }

        .empty-state {
            padding: 32px;
            border-radius: 28px;
            background: rgba(15,23,42,0.80);
            border: 1px solid rgba(148,163,184,0.14);
            margin-bottom: 18px;
        }

        .empty-kicker {
            color: #A78BFA;
            font-size: 12px;
            font-weight: 950;
            letter-spacing: 0.12em;
            margin-bottom: 12px;
        }

        .empty-title {
            color: #FFFFFF;
            font-size: 34px;
            line-height: 1.12;
            letter-spacing: -0.05em;
            font-weight: 950;
            margin-bottom: 12px;
        }

        .empty-text {
            color: #CBD5E1;
            font-size: 17px;
            line-height: 1.7;
            max-width: 780px;
        }

        [data-testid="stMetric"] {
            background: rgba(15,23,42,0.78);
            border: 1px solid rgba(148,163,184,0.16);
            border-radius: 24px;
            padding: 22px;
            box-shadow: 0 18px 50px rgba(0,0,0,0.20);
        }

        [data-testid="stDataFrame"] {
            border-radius: 22px;
            overflow: hidden;
            border: 1px solid rgba(148,163,184,0.14);
        }

        [data-baseweb="select"] > div {
            background: rgba(15,23,42,0.82) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(148,163,184,0.14) !important;
        }

        .stMultiSelect label {
            color: #CBD5E1 !important;
            font-weight: 700 !important;
        }

        h1, h2, h3, h4, p, div, span, label {
            color: #F8FAFC;
        }

        hr {
            border-color: rgba(148,163,184,0.14);
        }

        @media (max-width: 1000px) {
            .hero-wrapper {
                grid-template-columns: 1fr;
            }

            .hero-title {
                font-size: 48px;
            }

            .insight-grid {
                grid-template-columns: 1fr;
            }

            .decision-grid {
                grid-template-columns: 1fr 1fr;
            }

            .friction-body {
                grid-template-columns: 1fr;
            }

            .friction-header {
                flex-direction: column;
            }

            .premium-card {
                height: auto;
                min-height: 320px;
            }
        }

        @media (max-width: 700px) {
            .decision-grid {
                grid-template-columns: 1fr;
            }

            .friction-title {
                font-size: 28px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )