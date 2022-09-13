import random

from requests.exceptions import SSLError

from src.yaml.plugin import Plugin
import requests
from bs4 import BeautifulSoup, element
from src.config import config as global_config


class Entertainment(Plugin):
    translations = {
        'not_found': {
            'de': 'Ich habe leider nichts gefunden...',
            'en': 'Nothing found...'
        },
        'error_request': {
            'de': 'Fehler beim laden eines Witzes',
            'en': 'Error loading a joke'
        }
    }

    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)
        self.jokes = {
            'de': [self.__jokes_lustige_sprueche_net],
            'en': []
        }
        self.language = global_config.language

    @staticmethod
    def __jokes_lustige_sprueche_net():
        categories = ['coronavirus-sprueche', 'dumme-sprueche', 'chuck-norris-sprueche', 'quarantaene-sprueche',
                      'veganer-sprueche', 'saufsprueche', 'nerd-witze', 'trinksprueche']
        jokes = []
        index_method = random.randint(0, len(categories) - 1)
        try:
            response = requests.get('https://www.lustige-sprueche.net/{0}'.format(categories[index_method]))
        except SSLError:
            return Entertainment.translations['error_request']
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find_all(class_='click_snippet_link_element')
        for joke in result:
            assert isinstance(joke, element.Tag)
            elem = joke.find_previous('a')
            if 'title' in elem.attrs:
                jokes.append(elem.attrs['title'])
        return jokes

    def __jokes(self):
        if len(self.jokes[self.language]) > 0:
            index_method = random.randint(0, len(self.jokes[self.language]) - 1)
            jokes = self.jokes[self.language][index_method]()
            index_jokes = random.randint(0, len(jokes) - 1)
            return jokes[index_jokes]
        return self.translations['not_found'][self.language]

    def make_jokes(self, args):
        answer = self.__jokes()
        return {'$joke': answer}

    def user_is_boring(self, args):
        answer = self.__jokes()
        return {'$response': answer}
