import streamlit as st
import pandas as pd


def show_backlog_table(df: pd.DataFrame):
    st.dataframe(
        df[["priority", "theme", "volume", "volume_share", "impact", "negative_rate", "blocking_incidents", "recommendation"]],
        use_container_width=True,
        hide_index=True,
    )


def show_verbatims(df: pd.DataFrame):
    cols = ["priority", "theme", "sentiment", "channel", "text", "matched_keywords", "theme_confidence"]
    st.dataframe(df[cols], use_container_width=True, hide_index=True)
