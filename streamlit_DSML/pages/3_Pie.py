import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Pie Chart", page_icon="🥧")

# Find the CSV relative to the repo root so it works locally and on Streamlit Cloud
CSV_PATH = Path(__file__).parent.parent / "data" / "pie_demo.csv"

st.title("How I Spend My Day")
st.write("This pie chart reads from `data/pie_demo.csv`. Use the controls below to explore it.")

df = pd.read_csv(CSV_PATH)

# Interactive controls
selected = st.multiselect(
    "Choose categories to include:",
    options=df["Category"].tolist(),
    default=df["Category"].tolist(),
)
donut = st.checkbox("Show as donut chart")

filtered = df[df["Category"].isin(selected)]

if filtered.empty:
    st.warning("Pick at least one category.")
else:
    fig = px.pie(
        filtered,
        names="Category",
        values="Value",
        title="Hours in a Typical Day",
        hole=0.4 if donut else 0,
    )
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("See the raw data"):
        st.dataframe(filtered, use_container_width=True)
