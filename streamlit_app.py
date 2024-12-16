import streamlit as st
import pandas as pd
from myfuns import genres, get_displayed_movies, get_popular_movies, get_recommended_movies

# using bootstrap theme
st.set_page_config(page_title="Movie Recommender", page_icon=":movie_camera:",
                   layout="wide", initial_sidebar_state="expanded")

# Sidebar for navigation
with st.sidebar:
    st.markdown("""
        <style>
        [data-testid="stSidebar"][aria-expanded="true"]{
            min-width: 250px;
            max-width: 250px;
        }
        </style>
        """, unsafe_allow_html=True)
    st.title("Movie Recommender")
    page = st.radio(
        "Navigation",
        ["System 1 - Genre", "System 2 - Collaborative"],
        key="nav_radio",
        horizontal=True,
        label_visibility="collapsed",
    )

# Function to display movie cards


def display_movie_card(movie, with_rating=False):
    container = st.container()
    with container:
        st.image(f"MovieImages/{movie.movie_id}.jpg", width=150)
        st.markdown(f"<div style='height: 50px; font-size: 0.7em'>{
                    movie.title}</div>", unsafe_allow_html=True)
        if with_rating:
            rating = st.radio("Rating", [1, 2, 3, 4, 5],
                              key=f"rating_{movie.movie_id}",
                              horizontal=True,
                              label_visibility="collapsed")
            return rating
    return None


# Initialize session state for user ratings
if 'user_ratings' not in st.session_state:
    st.session_state.user_ratings = {}

# System 1 - Genre
if page == "System 1 - Genre":
    st.title("Select a genre")
    genre = st.selectbox("Choose a genre", genres)
    if genre:
        popular_movies = get_popular_movies(genre)
        cols = st.columns(5)
        for idx, movie in popular_movies.iterrows():
            with cols[idx % 5]:
                display_movie_card(movie)


# System 2 - Collaborative
elif page == "System 2 - Collaborative":
    st.title("Rate some movies below to get recommendations")
    movies = get_displayed_movies()

    # Toggle between recommendation page and rating page
    recommended = False

    if st.button("Get recommendations"):
        # Clear the page
        st.empty()
        recommended = True
        # Fetch and display recommendations
        recommended_movies = get_recommended_movies(
            st.session_state.user_ratings)
        st.title("Your recommendations")

        # Display top 10 recommended movies in rows of 5
        rec_cols = st.columns(5)
        for idx, movie in recommended_movies.head(10).iterrows():
            with rec_cols[idx % 5]:
                display_movie_card(movie)

        if st.button("Try Again"):
            # Reset user ratings
            recommended = False
            st.session_state.user_ratings = {}
            st.experimental_rerun()

    if not recommended:
        # Display movies in rows of 5
        cols = st.columns(5)
        for idx, movie in movies.iterrows():
            with cols[idx % 5]:
                rating = display_movie_card(movie, with_rating=True)
                if rating:
                    st.session_state.user_ratings[movie.movie_id] = rating
