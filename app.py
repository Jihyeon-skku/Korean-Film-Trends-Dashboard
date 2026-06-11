import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Korean Film Trends Dashboard",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# Dark Trendy Style
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #050505 0%, #111111 45%, #1c1c1c 100%);
    color: white;
}

h1, h2, h3 {
    color: #ffffff;
}

.block-container {
    padding-top: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #111111;
}

.metric-card {
    background: linear-gradient(135deg, #1f1f1f, #2b2b2b);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #333333;
    box-shadow: 0 0 18px rgba(255, 255, 255, 0.05);
    text-align: center;
}

.metric-title {
    font-size: 15px;
    color: #aaaaaa;
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: #ff4b4b;
}

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    margin-bottom: 0px;
}

.subtitle {
    color: #bbbbbb;
    font-size: 18px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Movie Data
# -----------------------------
data = {
    "Movie": [
        "The Admiral: Roaring Currents", "Extreme Job", "Along with the Gods: The Two Worlds",
        "Ode to My Father", "Veteran", "The Thieves", "Miracle in Cell No. 7",
        "Assassination", "Masquerade", "A Taxi Driver", "Train to Busan", "The Host",
        "The Attorney", "Haeundae", "Parasite", "King and the Clown",
        "The Roundup", "The Outlaws", "12.12: The Day", "Exhuma",
        "I Can Speak", "Sunny", "Architecture 101", "My Sassy Girl",
        "Joint Security Area", "Silenced", "The Man from Nowhere", "New World",
        "Oldboy", "Decision to Leave", "Burning", "Broker",
        "The Wailing", "Snowpiercer", "1987: When the Day Comes",
        "Inside Men", "The Handmaiden", "Little Forest", "Swing Kids", "Exit"
    ],
    "Year": [
        2014, 2019, 2017, 2014, 2015, 2012, 2013,
        2015, 2012, 2017, 2016, 2006,
        2013, 2009, 2019, 2005,
        2022, 2017, 2023, 2024,
        2017, 2011, 2012, 2001,
        2000, 2011, 2010, 2013,
        2003, 2022, 2018, 2022,
        2016, 2013, 2017,
        2015, 2016, 2018, 2018, 2019
    ],
    "Genre": [
        "Historical", "Comedy", "Fantasy",
        "Drama", "Action", "Crime", "Drama",
        "Action", "Historical", "Historical", "Thriller", "Monster",
        "Drama", "Disaster", "Drama", "Historical",
        "Action", "Crime", "Historical", "Mystery",
        "Drama", "Comedy", "Romance", "Romance",
        "Drama", "Drama", "Action", "Crime",
        "Thriller", "Romance", "Drama", "Drama",
        "Horror", "Sci-Fi", "Historical",
        "Crime", "Thriller", "Drama", "Musical", "Comedy"
    ],
    "Audience": [
        17610000, 16260000, 14410000,
        14260000, 13410000, 12980000, 12810000,
        12700000, 12320000, 12180000, 11560000, 13010000,
        11370000, 11450000, 10310000, 10510000,
        12690000, 6880000, 13120000, 11910000,
        3280000, 7360000, 4110000, 4880000,
        5830000, 4660000, 6170000, 4680000,
        3260000, 1890000, 528000, 1260000,
        6870000, 9350000, 7230000,
        7070000, 4280000, 1500000, 1470000, 9420000
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# Title
# -----------------------------
st.markdown('<p class="main-title">🎬 Korean Film Trends Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Explore Korean movie trends through audience numbers, genres, release years, and box office performance.</p>',
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.title("🎛️ Filter Options")

search = st.sidebar.text_input("Search Movie Title")

genre_options = ["All"] + sorted(df["Genre"].unique().tolist())
selected_genre = st.sidebar.selectbox("Select Genre", genre_options)

year_range = st.sidebar.slider(
    "Select Year Range",
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

# -----------------------------
# KPI Cards
# -----------------------------
total_movies = len(filtered_df)
total_audience = filtered_df["Audience"].sum()
avg_audience = int(filtered_df["Audience"].mean()) if total_movies > 0 else 0
top_movie = filtered_df.sort_values("Audience", ascending=False).iloc[0]["Movie"] if total_movies > 0 else "No Data"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Movies</div>
        <div class="metric-value">{total_movies}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Audience</div>
        <div class="metric-value">{total_audience:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average Audience</div>
        <div class="metric-value">{avg_audience:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Top Movie</div>
        <div class="metric-value" style="font-size:20px;">{top_movie}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# Charts
# -----------------------------
if total_movies == 0:
    st.warning("No movies found. Please change your filter options.")

else:
    st.subheader("🏆 Top 10 Korean Movies by Audience")

    top10 = filtered_df.sort_values("Audience", ascending=False).head(10)
    top10_chart = top10.sort_values("Audience", ascending=True)

    fig_bar = px.bar(
        top10_chart,
        x="Audience",
        y="Movie",
        color="Genre",
        orientation="h",
        text="Audience",
        title="Top 10 Movies"
    )

    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(size=22)
    )

    fig_bar.update_traces(texttemplate="%{text:,}", textposition="outside")

    st.plotly_chart(fig_bar, use_container_width=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🎭 Genre Distribution")

        genre_data = filtered_df["Genre"].value_counts().reset_index()
        genre_data.columns = ["Genre", "Count"]

        fig_pie = px.pie(
            genre_data,
            names="Genre",
            values="Count",
            hole=0.45,
            title="Genre Share"
        )

        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.subheader("📈 Yearly Audience Trend")

        yearly = filtered_df.groupby("Year")["Audience"].sum().reset_index()

        fig_line = px.line(
            yearly,
            x="Year",
            y="Audience",
            markers=True,
            title="Total Audience by Year"
        )

        fig_line.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("📋 Movie Data Table")

    st.dataframe(
        filtered_df.sort_values("Audience", ascending=False),
        use_container_width=True
    )

    st.subheader("💡 Key Insight")

    most_popular_genre = filtered_df["Genre"].value_counts().idxmax()
    best_year = filtered_df.groupby("Year")["Audience"].sum().idxmax()

    st.write(
        f"The most common genre in the selected data is **{most_popular_genre}**. "
        f"The strongest year by total audience is **{best_year}**."
    )
