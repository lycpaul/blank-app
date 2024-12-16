import pandas as pd
import requests


class Recommender:
    def __init__(self):
        # Define the URL for movie data
        movies_url = "https://github.com/lycpaul/movie-ibcf/blob/main/MovieData/movies.dat?raw=true"
        
        # Fetch the data from the URL
        response = requests.get(movies_url)

        # Split the data into lines and then split each line using "::"
        movie_lines = response.text.split('\n')
        movie_data = [line.split("::") for line in movie_lines if line]

        # Create a DataFrame from the movie data
        self.movies = pd.DataFrame(
            movie_data, columns=['movie_id', 'title', 'genres'])
        self.movies['movie_id'] = self.movies['movie_id'].astype(int)

        self.genres = list(
            sorted(set([genre for genres in self.movies.genres.unique()
                   for genre in genres.split("|")]))
        )

    def get_displayed_movies(self):
        return self.movies.head(100)

    def get_recommended_movies(self, new_user_ratings):
        return self.movies.head(10)

    def get_popular_movies(self, genre: str):
        if genre == self.genres[1]:
            return self.movies.head(10)
        else:
            return self.movies[10:20]


if __name__ == "__main__":
    # testing
    recommender = Recommender()
    print(recommender.get_displayed_movies())
