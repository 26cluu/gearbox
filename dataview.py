import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

# 9.11
@st.cache_resource
def show_df():
    st.dataframe(df)

@st.cache_data
def fetch_data():
    df = pd.read_csv("car_prices.csv", on_bad_lines = "warn")
    df.dropna()
    return df

@st.cache_resource
def plot_lines(x_input, y_input):
    fig = plt.figure(figsize = (10, 4))
    sns.lineplot(data = df, x = x_input, y = y_input)
    sns.set(rc={'axes.facecolor': '#0d1118', 'figure.facecolor': '#0d1118', 'axes.labelcolor': 'white', 'text.color': 'white', 'xtick.color': 'white', 'ytick.color': 'white'})
    st.pyplot(fig)

@st.cache_resource
def plotBarColorGraph():
    color_counts = df['color'].value_counts()
    
    fig, ax = plt.subplots()

    sns.barplot(x=color_counts.index, y=color_counts.values, ax = ax)

    ax.set_xlabel('Color')
    ax.set_ylabel('Number of Cars')
    ax.set_title('Number of Cars per Color')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

@st.cache_resource
def plotAutoManual():
    transmission_counts = df['transmission'].value_counts()
    fig, ax = plt.subplots()

    sns.barplot(x=transmission_counts.index, y=transmission_counts.values, ax = ax)

    ax.set_xlabel('Type of Transmission')
    ax.set_ylabel('Number of Carss')
    ax.set_title('Automatic vs Manual Transmission')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

@st.cache_resource
def plotTransmissionCost():
    sns.scatterplot(data=df, x='year', y='sellingprice', hue='transmission', style='transmission')
    plt.xlabel('Year')
    plt.ylabel('Price')
    plt.title('Price Comparison of Manual vs Automatic Cars')
    plt.tight_layout()
    plt.gca().set_aspect('auto')

    min_year = df['year'].min()
    max_year = df['year'].max()
    x_range = max_year - min_year
    plt.xlim(min_year - 0.1 * x_range, max_year + 0.1 * x_range)

    st.pyplot(plt.gcf())


st.set_page_config(layout="wide")
df = fetch_data()
st.title("Used Cars Data")
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Data", "Year vs Condition", "Price vs Condition", "Year vs Odometer", "Cars per Color", "Auto vs Manual Popularity", "Auto vs Manual Price"])
with tab1:
    show_df()
with tab2:
    plot_lines('year', 'condition')
with tab3:
    plot_lines('sellingprice', 'condition')
with tab4:
    plot_lines('year', 'odometer')
with tab5:
    plotBarColorGraph()
with tab6:
    plotAutoManual()
with tab7:
    plotTransmissionCost()


    