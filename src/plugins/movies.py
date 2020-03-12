from imdb.Movie import Movie
from imdb.Person import Person
from src.yaml.plugin import Plugin
from imdb import IMDb


class Movies(Plugin):
    max_cast_count = 7
    max_movies_count = 10

    def __init__(self, name, config):
        super().__init__(name, config)
        self.imdb = IMDb()

    def __get_movie(self, movie_name):
        movies_list = self.imdb.search_movie(movie_name)
        movie = movies_list[0]
        movie = self.imdb.get_movie(movie.getID())
        assert isinstance(movie, Movie)
        return movie

    def __get_actor(self, actor_name):
        actor = self.imdb.search_person(actor_name)
        actor = self.imdb.get_person(actor[0].getID())
        assert isinstance(actor, Person)
        return actor

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
        plot = ''
        length = 0
        for i in range(0, len(movie['plot']) if len(movie['plot']) < 3 else 3):
            if len(movie['plot'][i]) > length:
                plot = movie['plot'][i]

        plot = plot.replace('::', '\n- __') + '__'

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

    def actor_details(self, args):
        self.requiere_param(args, '$actor')
        actor_name = args['$actor']

        actor = self.__get_actor(actor_name)

        filmography = actor['filmography']

        movies = ''
        for movie in filmography:
            for key in movie:
                counter = 0
                if 'actor' == key or 'actress' == key:
                    movies += '\n**Schauspieler**:'
                    for actor_movie in movie[key]:
                        if counter < self.max_movies_count:
                            movies += '\n- {0}'.format(str(actor_movie))
                            counter += 1
                        else:
                            break
                elif 'producer' == key:
                    movies += '\n**Producer**:'
                    for producer_movie in movie[key]:
                        if counter < self.max_movies_count:
                            movies += '\n- {0}'.format(str(producer_movie))
                            counter += 1
                        else:
                            break
                elif 'director' == key:
                    movies += '\n**Director**:'
                    for director_movie in movie[key]:
                        if counter < self.max_movies_count:
                            movies += '\n- {0}'.format(str(director_movie))
                            counter += 1
                        else:
                            break

        return {'$details': movies}
