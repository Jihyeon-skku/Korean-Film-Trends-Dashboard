import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote

st.set_page_config(
    page_title="Korean Film Trends Dashboard",
    page_icon="🎬",
    layout="wide"
)

# Dark Theme CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #050505, #141414, #1f1f1f);
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #111111;
}
h1, h2, h3 {
    color: white;
}
.movie-card {
    background-color: #181818;
    padding: 15px;
    border-radius: 15px;
    border: 1px solid #333;
    text-align: center;
    margin-bottom: 20px;
}
.movie-title {
    font-size: 16px;
    font-weight: bold;
    color: white;
}
.movie-info {
    font-size: 13px;
    color: #bbbbbb;
}
</style>
""", unsafe_allow_html=True)

# Load Data
df = pd.read_csv("korean_movies_top100.csv")

st.title("🎬 Korean Film Trends Dashboard")
st.write("Explore Korean film trends through box office performance, genres, release years, and audience numbers.")

# Sidebar
st.sidebar.header("🎛️ Filters")

search = st.sidebar.text_input("🔍 Search Movie Title")

genre_list = ["All"] + sorted(df["Genre"].unique().tolist())
selected_genre = st.sidebar.selectbox("🎭 Genre", genre_list)

year_range = st.sidebar.slider(
    "📅 Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Movie"].str.contains(search, case=False, na=False)
    ]

if selected_genre != "All":
    filtered_df = filtered_df[filtered_df["Genre"] == selected_genre]

filtered_df = filtered_df[
    (filtered_df["Year"] >= year_range[0]) &
    (filtered_df["Year"] <= year_range[1])
]

# KPI
col1, col2, col3 = st.columns(3)

col1.metric("Total Movies", len(filtered_df))
col2.metric("Total Audience", f"{filtered_df['Audience'].sum():,}")
col3.metric(
    "Average Audience",
    f"{int(filtered_df['Audience'].mean()):,}" if len(filtered_df) > 0 else "0"
)

st.divider()

if len(filtered_df) == 0:
    st.warning("No movies found. Please change your filters.")

else:
    # Top 10 Chart
    st.subheader("🏆 Top 10 Korean Movies by Audience")

    top10 = filtered_df.sort_values("Audience", ascending=False).head(10)
    top10_chart = top10.sort_values("Audience", ascending=True)

    fig = px.bar(
        top10_chart,
        x="Audience",
        y="Movie",
        color="Genre",
        orientation="h",
        text="Audience"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    fig.update_traces(texttemplate="%{text:,}")

    st.plotly_chart(fig, use_container_width=True)

    # Genre and Year Charts
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🎭 Genre Distribution")
        genre_data = filtered_df["Genre"].value_counts().reset_index()
        genre_data.columns = ["Genre", "Count"]

        fig2 = px.pie(
            genre_data,
            names="Genre",
            values="Count",
            hole=0.45
        )

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig2, use_container_width=True)

    with col_right:
        st.subheader("📈 Yearly Audience Trend")
        yearly = filtered_df.groupby("Year")["Audience"].sum().reset_index()

        fig3 = px.line(
            yearly,
            x="Year",
            y="Audience",
            markers=True
        )

        fig3.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig3, use_container_width=True)

    # Poster Cards
    st.subheader("🎞️ Movie Poster Gallery")

    poster_df = filtered_df.sort_values("Audience", ascending=False).head(24)

    cols = st.columns(4)

    for index, row in poster_df.iterrows():
        movie_title = row["Movie"]
        poster_url = f"https://placehold.co/300x450/111111/FFFFFF?text={quote(movie_title)}"

        with cols[index % 4]:
            st.markdown(
                f"""
                <div class="movie-card">
                    <img src="{poster_url}" width="100%" style="border-radius:12px;">
                    <p class="movie-title">{movie_title}</p>
                    <p class="movie-info">{row['Year']} · {row['Genre']}</p>
                    <p class="movie-info">Audience: {row['Audience']:,}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Data Table
    st.subheader("📋 Movie Data Table")

    st.dataframe(
        filtered_df.sort_values("Audience", ascending=False),
        use_container_width=True
    )
