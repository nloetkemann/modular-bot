import logging
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from src.yaml.plugin import Plugin
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


class Maps(Plugin):
    token_required = True
    max_restarts = 2
    actual_restarts = 0

    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)
        self.geolocator = Nominatim(user_agent="BotMap")

    def __get_city(self, city_name):
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
        self.requiere_param(args, '$start', '$end')
        start = args['$start']
        end = args['$end']

        start_location = self.__get_city(start)
        end_location = self.__get_city(end)

        distance = self.__get_distance(start_location, end_location)

        return {'$distance': '{:.2f}'.format(distance.kilometers)}
