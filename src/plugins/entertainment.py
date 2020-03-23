import random

from src.yaml.plugin import Plugin
import requests
from bs4 import BeautifulSoup, element


class Entertainment(Plugin):
    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)
        self.jokes = [self.__jokes_lustige_sprueche_net]

    @staticmethod
    def __jokes_lustige_sprueche_net():
        categories = ['coronavirus-sprueche', 'dumme-sprueche', 'chuck-norris-sprueche', 'quarantaene-sprueche',
                      'veganer-sprueche', 'saufsprueche', 'nerd-witze', 'trinksprueche']
        jokes = []
        index_method = random.randint(0, len(categories) - 1)
        response = requests.get('https://www.lustige-sprueche.net/{0}'.format(categories[index_method]))
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find_all(class_='click_snippet_link_element')
        for joke in result:
            assert isinstance(joke, element.Tag)
            elem = joke.find_previous('a')
            if 'title' in elem.attrs:
                jokes.append(elem.attrs['title'])
        return jokes

    def __jokes(self):
        index_method = random.randint(0, len(self.jokes) - 1)
        jokes = self.jokes[index_method]()
        index_jokes = random.randint(0, len(jokes) - 1)
        return jokes[index_jokes]

    def make_jokes(self, args):
        answer = self.__jokes()
        return {'$joke': answer}

    def user_is_boring(self, args):
        answer = self.__jokes()
        return {'$response': answer}
