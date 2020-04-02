import os
from src.exceptions.not_found_exception import NotFoundException
from src.tools.tools import Tools


class Translation:
    translation = None

    def __init__(self, plugin_list_name: {str: str}, translation_dir: str):
        if not os.path.exists(translation_dir):
            raise NotFoundException('Path: ' + translation_dir)
        self.path = translation_dir
        self.plugins_list_name = plugin_list_name.lower()
        self.__load_translation(self.plugins_list_name)

    def __load_translation(self, plugins_name: str):
        translation_path = self.path + '/' + plugins_name + '.yaml'
        translation = Tools.read_config_file(translation_path)
        self.translation = translation[plugins_name]

    def __get_translation(self,  keyword: str, category: str, language: str):
        print(keyword, category, language)
        for other in self.translation[category]:
            print(other)
            for key in other:
                if key == keyword:
                    print(key)
                    print(self.translation[category][other])
                    # return self.translation[category][other][keyword][language]
        return ''

    def get_keyword_translation(self, keyword: str, language: str):
        return self.__get_translation(keyword, 'keywords', language)

    def get_answer_translation(self, keyword: str, language: str):
        return self.__get_translation(keyword, 'answers', language)

    def get_other_translation(self, keyword: str, language: str):
        return self.__get_translation(keyword, 'other', language)
