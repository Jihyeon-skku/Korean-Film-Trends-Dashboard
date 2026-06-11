
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Korean Film Trends Dashboard",
    page_icon="🎬",
    layout="wide"
)

df = pd.read_csv("korean_movies.csv")

st.title("🎬 Korean Film Trends Dashboard")

st.write(
    "Explore Korean movie trends through audience numbers, genres, and yearly performance."
)

# Sidebar
genre = st.sidebar.selectbox(
    "Genre",
    ["All"] + list(df["Genre"].unique())
)

if genre != "All":
    df = df[df["Genre"] == genre]

# KPI
col1, col2, col3 = st.columns(3)

col1.metric(
    "Movies",
    len(df)
)

col2.metric(
    "Total Audience",
    f"{df['Audience'].sum():,}"
)

col3.metric(
    "Average Audience",
    f"{int(df['Audience'].mean()):,}"
)

# Top Movies
st.subheader("Top Korean Movies")

fig = px.bar(
    df.sort_values("Audience"),
    x="Audience",
    y="Movie",
    orientation="h",
    color="Genre"
)

st.plotly_chart(fig, use_container_width=True)

# Genre Distribution
st.subheader("Genre Distribution")

genre_data = df["Genre"].value_counts().reset_index()
genre_data.columns = ["Genre", "Count"]

fig2 = px.pie(
    genre_data,
    names="Genre",
    values="Count",
    hole=0.4
)

st.plotly_chart(fig2, use_container_width=True)

# Year Trend
st.subheader("Audience Trend by Year")

yearly = df.groupby("Year")["Audience"].sum().reset_index()

fig3 = px.line(
    yearly,
    x="Year",
    y="Audience",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# Table
st.subheader("Movie Dataset")

st.dataframe(df)
