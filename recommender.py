import pandas as pd
import requests
import numpy as np


class Recommender:
    def __init__(self):
        # normalized ratings
        self.popularity = pd.read_csv('matrix/popularity.csv')
        self.genres = list(
            sorted(set([genre for genre in self.popularity.Genres.unique()])))

        # similarity matrix
        self.similarity = pd.read_csv(
            'matrix/similarity_top_100.csv', index_col=0)

    def get_displayed_movies(self):
        # get the top 100 most popular movies
        return self.popularity.head(100)

    def get_popular_movies(self, genre: str):
        # get the top 10 most popular movies by genre
        return self.popularity[self.popularity['Genres'] == genre].head(10)

    def myIBCF(self, newuser: pd.Series) -> pd.Series:
        n = 10  # default number of recommendations
        w = newuser

        # compute the movie recommendations
        rated_movies = w[w.notna()].index
        rated_matrix = (~w.isna()).astype(int)
        w = w.fillna(0)
        recomendations = w.dot(self.similarity) / \
            rated_matrix.dot(self.similarity)
        recomendations = recomendations.sort_values(ascending=False)[
            0:n].dropna()

        # supplement the recommendations with the most popular movies
        if recomendations.size < n:
            print("supplementing recommendations with popular movies")
            # excluding the movies already rated by the user
            popular_movies = self.popularity[~self.popularity["MovieID"].isin(
                rated_movies)].head(n - recomendations.size)
            # append the popular movies to the recomendations
            recomendations = pd.concat([recomendations, pd.Series(data=popular_movies["rating_mean"].values,
                                        index=popular_movies["MovieID"].values)], axis=0)
        return recomendations

    def get_recommended_movies(self, newuser):
        print(newuser)

        # prepare the new user rating vector
        w = pd.Series(data=np.nan, index=self.similarity.columns)
        for key, value in newuser.items():
            w[key] = value
        recommendations = self.myIBCF(w)
        print(w, recommendations)
        
        # print the recommended movies
        df = self.popularity[self.popularity["MovieID"].isin(
            recommendations.index)]
        return df


if __name__ == "__main__":
    # testing
    recommender = Recommender()
    print(recommender.get_displayed_movies())

    print(recommender.similarity.shape)
    print(recommender.similarity.head())
