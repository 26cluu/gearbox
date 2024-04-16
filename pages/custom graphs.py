import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

@st.cache_data
def fetch_data():
    df = pd.read_csv("car_prices.csv", on_bad_lines = "warn")
    df.dropna()
    return df

df = fetch_data()

st.title("Custom Graphs")
x_input = st.selectbox("Pick a x value", ["sellingprice", "odometer", "mmr", "condition", "year"])
y_input = st.selectbox("Pick a y value", ["condition", "odometer", "mmr", "sellingprice", "year"])

col1, col2 = st.columns(2)

with col1:
    x_agregate = st.toggle("Agregate X Data")
    x_type = None

    if x_agregate:
        x_type = st.radio(
            "What type of x agregation would you like",
            ["mean", "median", "min", "max"]
        )

with col2:
    y_agregate = st.toggle("Agregate Y Data")
    y_type = None

    if y_agregate:
        y_type = st.radio(
            "What type of y agregation would you like",
            ["mean", "median", "min", "max"]
        )

if x_type != None:
    x = alt.X(field = x_input, scale = alt.Scale(), aggregate = x_type)
else:
    x = alt.X(field = x_input, scale = alt.Scale()) 

if y_type != None:
    y = alt.Y(field=y_input, aggregate = y_type, scale=alt.Scale(reverse = True))
else:
    y = alt.Y(field=y_input, scale=alt.Scale(reverse = True))
    

c = (
    alt.Chart(df)
    .mark_line()
    .encode(x = x, y = y)
    .properties(width = 1000, height = 700)
)

res = st.button("graph")
if res:
    st.altair_chart(c, theme = "streamlit", use_container_width=False)
