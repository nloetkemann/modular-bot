from src.yaml.plugin import Plugin
from src.config import config as global_config
import wikipedia


class Wiki(Plugin):

    def __init__(self, name, config):
        super().__init__(name, config)
        if global_config.env_value_exists('language'):
            wikipedia.set_lang(global_config.get_env('language'))
        else:
            wikipedia.set_lang('de')

    @staticmethod
    def cut_result(result, end):
        part_of_result = result[:end]
        sentences = part_of_result.split('.')
        if len(sentences) > 2:
            sentences.pop()
            return sentences
        else:
            return Wiki.cut_result(result, end + 100)

    @staticmethod
    def __get_summary(keyword: str, end: int = 600):
        result = wikipedia.summary(keyword)
        return '. '.join(Wiki.cut_result(result, end))

    def search_wiki(self, args: dict):
        """
        performes a search at wiki
        :param args: the params in format {$searchKeyword: 'value'}
        :return: the result of the search
        """
        self.requiere_param(args, '$searchKeyword')
        search_keyword = args['$searchKeyword']
        return {'$result': self.__get_summary(search_keyword).replace('*', r'\*')}
