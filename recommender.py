import pandas as pd
import requests


class Recommender:
    def __init__(self):
        # weighted ratings
        self.ratings = pd.read_csv('data/normalized_rating_sorted.csv')
        self.genres = list(
            sorted(set([genre for genre in self.ratings.Genres.unique()])))

    def get_displayed_movies(self):
        # get the top 100 most popular movies
        return self.ratings.head(100)

    def get_recommended_movies(self, new_user_ratings):
        # get the top 10 most popular movies
        return self.ratings.head(10)

    def get_popular_movies(self, genre: str):
        # get the top 10 most popular movies by genre
        return self.ratings[self.ratings['Genres'] == genre].head(10)


if __name__ == "__main__":
    # testing
    recommender = Recommender()
    print(recommender.get_displayed_movies())

    print(recommender.ratings.head())
