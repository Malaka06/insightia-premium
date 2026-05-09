import plotly.express as px
import streamlit as st


def theme_bar(df):
    counts = df["theme"].value_counts().reset_index()
    counts.columns = ["theme", "volume"]
    fig = px.bar(counts, x="theme", y="volume", title="Top irritants détectés", text="volume")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)


def sentiment_donut(df):
    counts = df["sentiment"].value_counts().reset_index()
    counts.columns = ["sentiment", "volume"]
    fig = px.pie(counts, names="sentiment", values="volume", hole=.55, title="Répartition sentiment")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)


def channel_bar(df):
    counts = df.groupby(["channel", "sentiment"]).size().reset_index(name="volume")
    fig = px.bar(counts, x="channel", y="volume", color="sentiment", title="Canal × sentiment", barmode="group")
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
