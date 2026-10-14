import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
import ast
import urllib.parse
import os
from dotenv import load_dotenv

# ---------------------------------------------------------
# Environment Variables (API keys & secrets live in .env)
# ---------------------------------------------------------
load_dotenv()

try:
    if hasattr(st, "secrets"):
        DEFAULT_TMDB_API_KEY = st.secrets.get("TMDB_API_KEY", os.getenv("TMDB_API_KEY", ""))
        DEFAULT_OMDB_API_KEY = st.secrets.get("OMDB_API_KEY", os.getenv("OMDB_API_KEY", "trilogy"))
    else:
        DEFAULT_TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
        DEFAULT_OMDB_API_KEY = os.getenv("OMDB_API_KEY", "trilogy")
except Exception:
    DEFAULT_TMDB_API_KEY = os.getenv("TMDB_API_KEY", "")
    DEFAULT_OMDB_API_KEY = os.getenv("OMDB_API_KEY", "trilogy")

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="MovieMatch - Personalized Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom CSS for Premium Cinema Experience
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    h1, h2, h3, h4, .cinema-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
    }

    /* Main Container & Gradient Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(26, 20, 50, 0.8) 0%, rgba(13, 17, 23, 0.95) 90%), #0b0e14;
        color: #e6edf3;
    }

    /* Header Banner */
    .hero-header {
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.25) 0%, rgba(0, 210, 255, 0.2) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .hero-title {
        font-size: 2.5rem;
        color: #7dd3fc;
        background: linear-gradient(90deg, #ff7eb3, #ff758c, #70a6ff, #00e5ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        color: #9aa5b5;
        font-size: 1.05rem;
        margin-top: 8px;
    }

    /* Movie Spotlight Card */
    .spotlight-card {
        background: rgba(22, 27, 34, 0.85);
        border: 1px solid rgba(138, 43, 226, 0.35);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(138, 43, 226, 0.15);
        backdrop-filter: blur(10px);
    }

    /* Recommendation Cards */
    .movie-card {
        background: rgba(22, 27, 34, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
    }

    .movie-card:hover {
        transform: translateY(-6px);
        border-color: rgba(0, 229, 255, 0.5);
        box-shadow: 0 12px 28px rgba(0, 229, 255, 0.2);
    }

    .match-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        font-weight: 700;
        font-size: 0.75rem;
        padding: 4px 10px;
        border-radius: 20px;
        margin-bottom: 8px;
    }

    .rating-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        font-weight: 600;
        font-size: 0.78rem;
        padding: 3px 8px;
        border-radius: 8px;
    }

    .genre-tag {
        display: inline-block;
        background: rgba(99, 102, 241, 0.18);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.3);
        font-size: 0.72rem;
        padding: 2px 7px;
        border-radius: 6px;
        margin-right: 4px;
        margin-bottom: 4px;
    }

    /* Colorful heading for Recommendation Controls (sidebar) */
    .controls-heading {
        color: #00e5ff;
        font-weight: 700;
        margin: 0 0 8px 0;
    }

    /* Per-card recommendation title (color set inline) */
    .rec-title {
        font-size: 1rem;
        font-weight: 700;
        margin: 2px 0 6px 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .rec-label-director { color: #00e5ff; font-weight: 600; }
    .rec-label-cast { color: #f472b6; font-weight: 600; }
    .rec-value { color: #cbd5e1; }

    .poster-container {
        width: 100%;
        aspect-ratio: 2/3;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 12px;
        background: #161b22;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(255,255,255,0.05);
    }

    .poster-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 10px;
        transition: transform 0.4s ease;
    }

    .poster-img:hover {
        transform: scale(1.04);
    }

    .poster-fallback {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100%;
        background: linear-gradient(145deg, #1c2333, #0d1117);
        padding: 16px;
        text-align: center;
        color: #8b949e;
    }

    /* Trailer Button */
    .trailer-btn {
        display: inline-block;
        width: 100%;
        text-align: center;
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white !important;
        font-weight: 600;
        font-size: 0.82rem;
        padding: 8px 12px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 10px;
        transition: opacity 0.2s ease;
    }
    .trailer-btn:hover {
        opacity: 0.9;
        text-decoration: none;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Sidebar widget labels: force high-contrast visible text */
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    section[data-testid="stSidebar"] .stWidgetLabel,
    section[data-testid="stSidebar"] [class*="stWidgetLabel"] {
        color: #00e5ff !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] label {
        color: #e6edf3 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] hr {
        border-color: rgba(255, 255, 255, 0.12);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Data Loading & Preprocessing (Cached)
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_and_prepare_data():
    # Load base processed dataset & similarity
    with open('movies.pkl', 'rb') as f:
        movies_df = pickle.load(f)

    with open('similarity.pkl', 'rb') as f:
        similarity_matrix = pickle.load(f)

    # Load rich metadata from TMDB raw datasets
    try:
        raw_movies = pd.read_csv('tmdb_5000_movies.csv')
        raw_credits = pd.read_csv('tmdb_5000_credits.csv')

        raw_movies = raw_movies.rename(columns={'id': 'movie_id'})
        
        # Merge movies metadata
        meta = raw_movies[['movie_id', 'vote_average', 'vote_count', 'release_date', 'genres', 'overview', 'tagline', 'runtime']].copy()
        merged = movies_df.merge(meta, on='movie_id', how='left')
        
        # Merge cast & crew
        credits_sub = raw_credits[['movie_id', 'cast', 'crew']].copy()
        merged = merged.merge(credits_sub, on='movie_id', how='left')

    except Exception:
        # Fallback if raw csvs not found
        merged = movies_df.copy()
        merged['vote_average'] = 7.0
        merged['release_date'] = '2015-01-01'
        merged['genres'] = '[]'
        merged['overview'] = ''
        merged['tagline'] = ''
        merged['runtime'] = 120
        merged['cast'] = '[]'
        merged['crew'] = '[]'

    # Helper to parse JSON lists
    def parse_genres(val):
        if not isinstance(val, str):
            return []
        try:
            items = ast.literal_eval(val)
            return [item['name'] for item in items if 'name' in item]
        except Exception:
            return []

    def parse_cast(val, top_n=3):
        if not isinstance(val, str):
            return []
        try:
            items = ast.literal_eval(val)
            return [item['name'] for item in items[:top_n] if 'name' in item]
        except Exception:
            return []

    def parse_director(val):
        if not isinstance(val, str):
            return 'Unknown'
        try:
            items = ast.literal_eval(val)
            for item in items:
                if item.get('job') == 'Director':
                    return item.get('name', 'Unknown')
        except Exception:
            pass
        return 'Unknown'

    def parse_year(val):
        if isinstance(val, str) and len(val) >= 4:
            return val[:4]
        return 'N/A'

    merged['genre_list'] = merged['genres'].apply(parse_genres)
    merged['top_cast'] = merged['cast'].apply(parse_cast)
    merged['director'] = merged['crew'].apply(parse_director)
    merged['year'] = merged['release_date'].apply(parse_year)
    merged['overview'] = merged['overview'].fillna('No overview available.')
    merged['vote_average'] = merged['vote_average'].fillna(0.0).round(1)

    return merged, similarity_matrix


# Load datasets
with st.spinner("Initializing MovieMatch Recommendation Engine..."):
    movies, similarity = load_and_prepare_data()


# ---------------------------------------------------------
# Poster Fetching Function (Auto TMDB + OMDb Fallback + Cache)
# ---------------------------------------------------------
@st.cache_data(show_spinner=False, ttl=86400)
def fetch_poster(movie_id, title="", year="", tmdb_api_key=""):
    api_key = tmdb_api_key.strip() if tmdb_api_key else DEFAULT_TMDB_API_KEY

    # 1. Official TMDB Poster Lookup
    if api_key:
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
            resp = requests.get(url, timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"
        except Exception:
            pass

    # 2. Secondary IMDb / OMDb High-Definition Poster Fetcher
    if title:
        try:
            clean_title = title.split(' (')[0].strip()
            params = {
                't': clean_title,
                'apikey': DEFAULT_OMDB_API_KEY
            }
            if year and year != 'N/A':
                params['y'] = year
            
            resp = requests.get("https://www.omdbapi.com/", params=params, timeout=2.5)
            if resp.status_code == 200:
                data = resp.json()
                poster = data.get('Poster')
                if poster and poster != 'N/A' and poster.startswith('http'):
                    return poster
        except Exception:
            pass

    return None


# ---------------------------------------------------------
# Recommendation Logic with Filtering & Match Score
# ---------------------------------------------------------
def get_recommendations(selected_title, top_k=5, selected_genre="All", min_rating=0.0):
    try:
        idx = movies[movies['title'] == selected_title].index[0]
    except IndexError:
        return []

    sim_scores = similarity[idx]
    
    # Sort indices by similarity descending (skipping the movie itself at index 0)
    sorted_indices = sorted(list(enumerate(sim_scores)), reverse=True, key=lambda x: x[1])

    results = []
    for candidate_idx, score in sorted_indices:
        if candidate_idx == idx:
            continue
        
        row = movies.iloc[candidate_idx]
        
        # Apply genre filter if specified
        if selected_genre != "All" and selected_genre not in row['genre_list']:
            continue
        
        # Apply rating filter
        if row['vote_average'] < min_rating:
            continue

        match_pct = max(0, min(100, int(score * 100)))

        results.append({
            'movie_id': row['movie_id'],
            'title': row['title'],
            'year': row['year'],
            'rating': row['vote_average'],
            'genres': row['genre_list'],
            'overview': row['overview'],
            'director': row['director'],
            'cast': row['top_cast'],
            'runtime': row['runtime'],
            'match_pct': match_pct,
            'similarity_raw': score
        })

        if len(results) >= top_k:
            break

    return results


# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<p class="controls-heading" style="font-size: 1.2rem;">⚙️ Recommendation Controls</p>', unsafe_allow_html=True)

    # API keys are loaded silently from .env (not shown to users)
    user_tmdb_key = ""

    st.markdown("---")
    
    # All distinct genres
    all_genres = sorted(list({g for glist in movies['genre_list'] for g in glist}))
    
    selected_genre_filter = st.selectbox(
        "🎭 Filter by Genre:",
        ["All"] + all_genres,
        index=0
    )

    num_recommendations = st.slider(
        "🎯 Number of Recommendations:",
        min_value=3,
        max_value=12,
        value=5,
        step=1
    )

    min_rating_filter = st.slider(
        "⭐ Minimum TMDB Rating:",
        min_value=0.0,
        max_value=9.0,
        value=0.0,
        step=0.5
    )

    st.markdown("---")
    
    # Quick Random Movie Surprise button
    if st.button("🎲 Surprise Me (Random Pick)", use_container_width=True):
        random_movie = movies.sample(1).iloc[0]['title']
        st.session_state['selected_movie'] = random_movie


# Default or session state movie
if 'selected_movie' not in st.session_state:
    st.session_state['selected_movie'] = movies['title'].iloc[0]


# ---------------------------------------------------------
# Hero Banner
# ---------------------------------------------------------
st.markdown("""
<div class="hero-header">
    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(0, 229, 255, 0.12); border: 1px solid rgba(0, 229, 255, 0.3); padding: 4px 14px; border-radius: 20px; margin-bottom: 12px;">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00e5ff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
        </svg>
        <span style="font-size: 0.75rem; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; color: #00e5ff;">Smart Recommendation Engine</span>
    </div>
    <h1 class="hero-title">MovieMatch</h1>
    <p class="hero-subtitle">
        Find movies that match your favorite stories, genres, and themes. Explore personalized recommendations and discover something new to watch.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Movie Selection Area
# ---------------------------------------------------------
col_select, col_btn = st.columns([4, 1], gap="small")

with col_select:
    all_titles = movies['title'].tolist()
    # Find current index in list
    current_index = all_titles.index(st.session_state['selected_movie']) if st.session_state['selected_movie'] in all_titles else 0

    selected_movie_name = st.selectbox(
        "🔍 Search or Select a Movie from Database:",
        options=all_titles,
        index=current_index,
        label_visibility="collapsed"
    )
    st.session_state['selected_movie'] = selected_movie_name

with col_btn:
    recommend_clicked = st.button("✨ Get Recommendations", type="primary", use_container_width=True)


# ---------------------------------------------------------
# Selected Movie Spotlight
# ---------------------------------------------------------
curr_movie_row = movies[movies['title'] == st.session_state['selected_movie']].iloc[0]
spotlight_poster = fetch_poster(curr_movie_row['movie_id'], title=curr_movie_row['title'], year=curr_movie_row['year'], tmdb_api_key=user_tmdb_key)

with st.container():
    col_spot_poster, col_spot_info = st.columns([1, 4], gap="medium")
    with col_spot_poster:
        if spotlight_poster:
            st.image(spotlight_poster, use_container_width=True)
        else:
            st.markdown(f"""
            <div class="poster-container" style="max-height: 240px; margin-bottom: 0;">
                <div class="poster-fallback">
                    <div style="font-size: 2.5rem; margin-bottom: 8px;">🎬</div>
                    <div style="font-weight: 700; font-size: 1rem; color: #fff;">{curr_movie_row['title']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_spot_info:
        st.markdown(f"""
        <div class="spotlight-card" style="margin-bottom: 0; padding: 18px 24px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; color: #a5b4fc; font-weight: 600;">Selected Movie Spotlight</span>
                    <h2 style="font-size: 1.7rem; margin: 4px 0 6px 0; color: #ffffff;">{curr_movie_row['title']} <span style="color: #8b949e; font-size: 1.1rem; font-weight: 400;">({curr_movie_row['year']})</span></h2>
                </div>
                <div>
                    <span class="rating-badge" style="font-size: 0.95rem; padding: 6px 12px;">★ {curr_movie_row['vote_average']} / 10</span>
                </div>
            </div>
            <div style="margin: 8px 0;">
                {''.join([f'<span class="genre-tag">{g}</span>' for g in curr_movie_row['genre_list']])}
            </div>
            <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5; margin-top: 6px;">
                {curr_movie_row['overview']}
            </p>
            <div style="margin-top: 10px; font-size: 0.82rem; color: #94a3b8; display: flex; gap: 20px; flex-wrap: wrap;">
                <span>🎬 <strong>Director:</strong> {curr_movie_row['director']}</span>
                <span>👥 <strong>Top Cast:</strong> {', '.join(curr_movie_row['top_cast']) if curr_movie_row['top_cast'] else 'N/A'}</span>
                <span>⏱️ <strong>Runtime:</strong> {int(curr_movie_row['runtime']) if pd.notnull(curr_movie_row['runtime']) else 'N/A'} min</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# Generate Recommendations
# ---------------------------------------------------------
recommendations = get_recommendations(
    selected_title=st.session_state['selected_movie'],
    top_k=num_recommendations,
    selected_genre=selected_genre_filter,
    min_rating=min_rating_filter
)

# ---------------------------------------------------------
# Tabs: Grid View vs Comparison & Insights
# ---------------------------------------------------------
tab_grid, tab_insights, tab_top_rated = st.tabs(["🍿 Top Recommendations", "📊 Similarity & Deep Dive", "🌟 Highest Rated in Catalog"])

with tab_grid:
    if not recommendations:
        st.warning(f"No recommendations found matching Genre: **{selected_genre_filter}** and Min Rating: **{min_rating_filter}★**. Try adjusting your filters in the sidebar!")
    else:
        st.markdown(f"### 🎯 Recommended for you based on <span style='color: #ff7eb3; font-weight: 700;'>{st.session_state['selected_movie']}</span>", unsafe_allow_html=True)

        # Distinct accent color per recommendation card
        title_palette = ['#00e5ff', '#ff7eb3', '#a78bfa', '#fbbf24', '#34d399', '#f87171', '#60a5fa', '#f472b6']
        
        # Determine number of columns dynamically (e.g. 5 columns or up to top_k)
        cols_per_row = 5
        for row_start in range(0, len(recommendations), cols_per_row):
            batch = recommendations[row_start:row_start + cols_per_row]
            cols = st.columns(cols_per_row)
            
            for i, movie in enumerate(batch):
                with cols[i]:
                    card_color = title_palette[(row_start + i) % len(title_palette)]
                    # Match badge hue shifts from red (low) to green (high)
                    match_hue = int(movie['match_pct'] * 1.2)
                    match_badge_style = f"background: linear-gradient(135deg, hsl({match_hue}, 70%, 45%) 0%, hsl({match_hue}, 70%, 32%) 100%);"

                    # Fetch poster using TMDB API with OMDb fallback
                    poster_url = fetch_poster(movie['movie_id'], title=movie['title'], year=movie['year'], tmdb_api_key=user_tmdb_key)
                    trailer_query = urllib.parse.quote(f"{movie['title']} {movie['year']} official trailer")
                    trailer_link = f"https://www.youtube.com/results?search_query={trailer_query}"
                    
                    genres_html = ''.join([f'<span class="genre-tag">{g}</span>' for g in movie['genres'][:2]])
                    cast_str = ', '.join(movie['cast'][:2]) if movie['cast'] else 'N/A'

                    # Native Streamlit Image Display (Guaranteed rendering)
                    if poster_url:
                        st.image(poster_url, use_container_width=True)
                    else:
                        st.markdown(f"""
                        <div class="poster-container" style="height: 250px;">
                            <div class="poster-fallback">
                                <div style="font-size: 2.2rem; margin-bottom: 8px;">🎬</div>
                                <div style="font-weight: 700; font-size: 0.95rem; color: #f1f5f9; line-height: 1.2;">{movie['title']}</div>
                                <div style="font-size: 0.75rem; color: #64748b; margin-top: 4px;">{movie['year']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 6px 0 4px 0;">
                        <span class="match-badge" style="{match_badge_style}">⚡ {movie['match_pct']}% Match</span>
                        <span class="rating-badge">★ {movie['rating']}</span>
                    </div>
                    <div class="rec-title" style="color: {card_color};" title="{movie['title']}">
                        {movie['title']}
                    </div>
                    <div style="margin-bottom: 6px;">
                        {genres_html}
                    </div>
                    <div style="font-size: 0.75rem; line-height: 1.4; margin-bottom: 8px;">
                        <span class="rec-label-director">Director:</span> <span class="rec-value">{movie['director']}</span><br>
                        <span class="rec-label-cast">Cast:</span> <span class="rec-value">{cast_str}</span>
                    </div>
                    <a href="{trailer_link}" target="_blank" class="trailer-btn">▶ Watch Trailer</a>
                    """, unsafe_allow_html=True)

                    # Expandable details
                    with st.expander("📖 Storyline"):
                        st.caption(movie['overview'])


with tab_insights:
    st.markdown("### 📊 Similarity & Matching Analytics")
    st.write("Explore how these recommendations match the core themes, genres, and metadata of the selected title.")
    
    if recommendations:
        comp_data = []
        for r in recommendations:
            comp_data.append({
                'Movie Title': r['title'],
                'Match Score': f"{r['match_pct']}%",
                'TMDB Rating': f"★ {r['rating']}",
                'Release Year': r['year'],
                'Director': r['director'],
                'Genres': ", ".join(r['genres']),
                'Top Cast': ", ".join(r['cast'])
            })
        
        comp_df = pd.DataFrame(comp_data)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        st.markdown("#### 💡 How the AI Engine Recommends Movies")
        st.info("""
        1. **Tag Synthesis:** Combined natural language tags extracted from movie overviews, genre keywords, top 3 actors, and the director.
        2. **Bag of Words & Vectorization:** Text stemmed and converted into a 5,000-dimensional frequency feature space.
        3. **Cosine Similarity Matrix:** Calculates the multi-dimensional cosine distance between all 4,800+ movies to rank the closest thematic matches.
        """)


with tab_top_rated:
    st.markdown("### 🌟 Highest Rated Classics in the TMDB 5000 Catalog")
    top_rated_df = movies[movies['vote_count'] > 1000].sort_values(by='vote_average', ascending=False).head(5)
    
    top_cols = st.columns(5)
    for idx, (_, top_m) in enumerate(top_rated_df.iterrows()):
        with top_cols[idx]:
            top_poster = fetch_poster(top_m['movie_id'], title=top_m['title'], year=top_m['year'], tmdb_api_key=user_tmdb_key)
            if top_poster:
                st.image(top_poster, use_container_width=True)
            st.markdown(f"""
            <div style="margin-top: 6px;">
                <span class="rating-badge">★ {top_m['vote_average']} / 10</span>
                <h4 style="font-size: 0.95rem; margin: 4px 0 2px 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{top_m['title']}</h4>
                <div style="font-size: 0.75rem; color: #8b949e;">{top_m['year']} • {top_m['director']}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>MovieMatch • Built with Python, Streamlit, Scikit-Learn & TMDB Dataset</div>", unsafe_allow_html=True)