import streamlit as st
import pandas as pd
from recommender import Recommender

# using bootstrap theme
st.set_page_config(page_title="Movie Recommender", page_icon=":movie_camera:",
                   layout="wide", initial_sidebar_state="expanded")

recommender = Recommender()

# Initialize session state for user ratings
if 'user_ratings' not in st.session_state:
    st.session_state.user_ratings = {}


# Toggle between recommendation page and rating page
if 'isRecommendPage' not in st.session_state:
    st.session_state.isRecommendPage = False

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


def display_movie_card(movie, with_rating=False):
    # Function to display movie cards
    container = st.container()
    with container:
        id_num = str(movie.MovieID).replace("m", "")
        st.image(f"MovieImages/{id_num}.jpg", width=150)
        st.markdown(f"<div style='height: 50px; font-size: 0.7em'>{
                    movie.Title}</div>", unsafe_allow_html=True)

        # Display the rating radio buttons
        if with_rating:
            rating = st.radio("Rating", [1, 2, 3, 4, 5],
                              key=f"rating_{movie.MovieID}",
                              horizontal=True,
                              label_visibility="collapsed",
                              index=None)
            return rating
    return None


# System 1 - Genre
if page == "System 1 - Genre":
    st.title("Popular movies by genre")
    genre = st.selectbox("Choose a genre", recommender.genres)
    if genre:
        popular_movies = recommender.get_popular_movies(genre)
        print(popular_movies)
        cols = st.columns(5)
        i = 0
        for idx, movie in popular_movies.iterrows():
            with cols[i % 5]:
                display_movie_card(movie)
            i += 1

# System 2 - Collaborative
elif page == "System 2 - Collaborative":
    st.title("Rate some movies!")
    movies = recommender.get_displayed_movies()

    def reset_ratings():
        """Callback function to reset user ratings and session state."""
        st.session_state.isRecommendPage = False
        st.session_state.user_ratings = {}
        print("reset user ratings", st.session_state.user_ratings)

    # Only enable recommendation button if there are ratings
    if st.button("Get recommendations"):
        # Clear the page
        st.empty()
        st.session_state.isRecommendPage = True

        # Fetch and display recommendations
        recommendations = recommender.get_recommended_movies(
            st.session_state.user_ratings)

        # Use callback for "Try Again" button
        st.button("Try Again", on_click=reset_ratings)

        # Display top 10 recommended movies
        st.write("Your recommendations")
        rec_cols = st.columns(5)
        for idx, movie in recommendations.head(10).iterrows():
            with rec_cols[idx % 5]:
                display_movie_card(movie)

    if not st.session_state.isRecommendPage:
        # Display movies rating
        cols = st.columns(5)
        for idx, movie in movies.iterrows():
            with cols[idx % 5]:
                rating = display_movie_card(movie, with_rating=True)
                if rating:
                    st.session_state.user_ratings[movie.MovieID] = rating
