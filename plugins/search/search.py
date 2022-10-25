import logging

from duckduckgo_search import ddg
from googlesearch import search
from src.yaml.plugin import Plugin
from src.config import config as global_config


class Search(Plugin):

    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)
        self.search_apis = {'duckduckgo': self._duckduckgo, 'google': self._google}
        if global_config.env_value_exists('search_api') and global_config.get_env('search_api') in self.search_apis:
            self.engine = self.search_apis[global_config.get_env('search_api')]
        else:
            self.engine = self.search_apis['duckduckgo']

    @staticmethod
    def _duckduckgo(search_query):
        result = ddg(search_query, safesearch='Moderate', max_results=10)
        hrefs = [item['href'] for item in result]
        return hrefs

    @staticmethod
    def _google(search_query):
        result = search(search_query, num_results=10, lang=global_config.language)
        return list(result)

    def search_query(self, args):
        self.requiere_param(args, '$query')
        result = self.engine(args['$query'])
        if len(result) > 0:
            content = '\n'.join(result)
        else:
            content = self.translation.get_other_translation('nothing_found', global_config.language)
        return {'$result': content}
