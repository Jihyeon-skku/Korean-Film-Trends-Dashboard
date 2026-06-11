import requests
import streamlit as st
import pandas as pd
import plotly.express as px
from urllib.parse import quote

st.set_page_config(
    page_title="Korean Film Trends Dashboard",
    page_icon="🎬",
    layout="wide"
)

# =============================
# Dark Theme CSS
# =============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #050505, #111111, #1c1c1c);
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #0b0b0b;
}

h1, h2, h3 {
    color: white;
}

.movie-card {
    background-color: #181818;
    padding: 14px;
    border-radius: 18px;
    border: 1px solid #333;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 0 18px rgba(255,255,255,0.05);
}

.movie-card:hover {
    transform: scale(1.02);
    transition: 0.2s;
    border: 1px solid #ff4b4b;
}

.movie-title {
    font-size: 16px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
}

.movie-info {
    font-size: 13px;
    color: #bbbbbb;
}
</style>
""", unsafe_allow_html=True)

# =============================
# Load Data
# =============================
df = pd.read_csv("korean_movies_top100.csv")

# =============================
# TMDB Poster Function
# =============================
TMDB_API_KEY = st.secrets["TMDB_API_KEY"]

@st.cache_data
def get_poster_url(movie_title):
    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title,
        "language": "en-US"
    }

    try:
        response = requests.get(url, params=params, timeout=5)

        if response.status_code == 200:
            results = response.json().get("results", [])

            if results:
                poster_path = results[0].get("poster_path")

                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except:
        pass

    return f"https://placehold.co/300x450/111111/FFFFFF?text={quote(movie_title)}"

# =============================
# Title
# =============================
st.title("🎬 Korean Film Trends Dashboard")
st.write(
    "Explore Korean film trends through box office performance, genres, release years, audience numbers, and real movie posters."
)

# =============================
# Sidebar Filters
# =============================
st.sidebar.header("🎛️ Filters")

search = st.sidebar.text_input("🔍 Search Movie Title")

genre_list = ["All"] + sorted(df["Genre"].dropna().unique().tolist())
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

# =============================
# KPI Cards
# =============================
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
    # =============================
    # Top 10 Chart
    # =============================
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

    # =============================
    # Genre + Year Charts
    # =============================
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

    # =============================
    # Poster Gallery
    # =============================
    st.subheader("🎞️ Movie Poster Gallery")

    poster_df = filtered_df.sort_values("Audience", ascending=False).head(24)

    cols = st.columns(4)

    for i, row in poster_df.reset_index(drop=True).iterrows():
        movie_title = row["Movie"]
        poster_url = get_poster_url(movie_title)

        with cols[i % 4]:
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

    # =============================
    # Data Table
    # =============================
    st.subheader("📋 Movie Data Table")

    st.dataframe(
        filtered_df.sort_values("Audience", ascending=False),
        use_container_width=True
    )
