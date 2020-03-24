import logging
from geopy import Location
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from src.plugins.wiki import Wiki
from src.yaml.plugin import Plugin
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class Maps(Plugin):
    max_restarts = 2
    actual_restarts = 0

    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)
        self.geolocator = Nominatim(user_agent="BotMap")

    @staticmethod
    def get_coordinates(city_name):
        geolocator = Nominatim()
        city = geolocator.geocode(city_name, timeout=5)
        assert isinstance(city, Location)
        return city.latitude, city.longitude, Maps.extract_plz(city)

    @staticmethod
    def extract_plz(city: Location):
        return city.raw['display_name'].split(',')[-2].strip()

    def __get_city(self, city_name):
        """
        :param city_name the name of the city
        :return the city by name
        """
        try:
            location = self.geolocator.geocode(city_name, timeout=3)
            self.actual_restarts = 0
            return location
        except GeocoderTimedOut as e:
            if self.actual_restarts <= self.max_restarts:
                logger.info('Plugin Maps restart geolocator')
                self.actual_restarts += 1
                return self.__get_city(city_name)
            else:
                raise e
        except GeocoderUnavailable:
            return ''

    def __get_distance(self, start, end):
        """
        :param start the city from where to start
        :param end the of the distance
        """
        try:
            distance = geodesic((start.latitude, start.longitude),
                                (end.latitude, end.longitude))
            self.actual_restarts = 0
            return distance
        except GeocoderTimedOut as e:
            if self.actual_restarts <= self.max_restarts:
                logger.info('Plugin Maps restart geodesic')
                self.actual_restarts += 1
                return self.__get_distance(start, end)
            else:
                raise e

    def calc_distance(self, args):
        """
        calcs the distance between two cities
        :param args format {$start: rahden, $end: epelkamp}
        :return in format {'$distance': 12)}
        """
        self.requiere_param(args, '$start', '$end')
        start = args['$start']
        end = args['$end']

        start_location = self.__get_city(start)
        end_location = self.__get_city(end)

        distance = self.__get_distance(start_location, end_location)

        return {'$distance': '{:.2f}'.format(distance.kilometers)}

    def city_info(self, args):
        """
        get some city infos
        :param args in format {$city: name}
        :return in format {'$result': infos}
        """
        self.requiere_param(args, '$city')

        city = self.__get_city(args['$city'])
        assert isinstance(city, Location)
        wiki_infos = Wiki.get_summary(city.address)

        infos = '\n{0}\nKoordinaten: {1}, {2}\n{3}'.format(city.address, city.latitude, city.longitude, wiki_infos)
        return {'$result': infos}
