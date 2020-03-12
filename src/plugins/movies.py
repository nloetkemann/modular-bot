from imdb.Movie import Movie

from src.yaml.plugin import Plugin
from imdb import IMDb


class Movies(Plugin):

    def __init__(self, name, config):
        super().__init__(name, config)
        self.imdb = IMDb()

    def get_movie_description(self, args: dict):
        """
        performes a search at wiki
        :param args: the params in format {$searchKeyword: 'value'}
        :return: the result of the search
        """
        self.requiere_param(args, '$movie')
        movies_list = self.imdb.search_movie(args['$movie'])
        movie = movies_list[0]
        assert isinstance(movie, Movie)
        plot = ''
        print(movie.getID())
        print(movie['year'])
        for key in movie:
            print(key)

        answer = '*{title}* ({year})\nGenres: {genres}'.format(title=movie['title'], year=movie['year'], genres=movie['cast'])
        # for plot in movies_list[0]['plot']:
        #     print(plot)
        return {'$movie': answer}
