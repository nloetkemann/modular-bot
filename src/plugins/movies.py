from imdb.Movie import Movie
from imdb.Person import Person
from src.yaml.plugin import Plugin
from imdb import IMDb


class Movies(Plugin):
    max_cast_count = 7

    def __init__(self, name, config):
        super().__init__(name, config)
        self.imdb = IMDb()

    def __get_movie(self, movie_name):
        movies_list = self.imdb.search_movie(movie_name)
        movie = movies_list[0]
        movie = self.imdb.get_movie(movie.getID())
        assert isinstance(movie, Movie)
        return movie

    def get_movie_description(self, args: dict):
        """
        performes a search at wiki
        :param args: the params in format {$searchKeyword: 'value'}
        :return: the result of the search
        """
        self.requiere_param(args, '$movie')
        movie = self.__get_movie(args['$movie'])
        title = movie['title']
        year = movie['year']
        plot = movie['plot'][0]

        plot = plot.replace('::', '__') + '__'

        answer = '**{title}** ({year}) handelt von:\n{plot}'.format(title=title, year=year, plot=plot)
        return {'$description': answer}

    def get_movie_cast(self, args):
        self.requiere_param(args, '$movie')
        movie = self.__get_movie(args['$movie'])

        title = movie['title']
        year = movie['year']
        cast = movie['cast']

        counter = 0
        all_cast = ''
        for actor in cast:
            assert isinstance(actor, Person)
            if counter < self.max_cast_count:
                all_cast += '\n- __{0}__ => {1}'.format(actor.currentRole, actor['name'])
                counter += 1
            else:
                break

        answer = '**{title}** ({year}) ist besetzt mit:{cast}'.format(title=title, year=year, cast=all_cast)
        return {'$cast': answer}
