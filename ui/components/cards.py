import streamlit as st


def kpi_card(label: str, value: str, help_text: str = ""):
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-value'>{value}</div>
        <div class='small-muted'>{help_text}</div>
    </div>
    """, unsafe_allow_html=True)


def glass_card(title: str, body: str, badge: str | None = None):
    badge_html = f"<span class='badge'>{badge}</span>" if badge else ""
    st.markdown(f"""
    <div class='glass-card'>
        {badge_html}
        <h3>{title}</h3>
        <p class='small-muted'>{body}</p>
    </div>
    """, unsafe_allow_html=True)
