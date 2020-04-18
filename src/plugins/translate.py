from src.yaml.plugin import Plugin
from translate import Translator
from src.config import config as global_config


class Translate(Plugin):
    language_keys = {
        'de': ['deutsch', 'german'],
        'en': ['englisch', 'english'],
        'fr': ['französisch', 'french'],
        'gr': ['griechisch', 'greek'],
        'is': ['isländisch', 'icelandic'],
        'ja': ['japanisch', 'japanese'],
        'lt': ['litauisch', 'lithuanian'],
        'zh': ['chinesisch', 'chinese'],
        'ru': ['russisch', 'russian']
    }

    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)

    def __get_language(self, language: str):
        for key in self.language_keys:
            if language in self.language_keys[key] or key == language:
                return key

        if len(language) == 2:
            return language

    @staticmethod
    def translate(content, base_language, target_language):
        translator = Translator(from_lang=base_language, to_lang=target_language)
        return translator.translate(content)

    def translate_from_default(self, args):
        self.requiere_param(args, '$content', '$language')
        content = args['$content']
        language = args['$language']
        base_language = global_config.language
        return {'$translation': '\n' + self.translate(content, base_language, self.__get_language(language))}

    def translate_into_language(self, args):
        self.requiere_param(args, '$content', '$base', '$target')
        content = args['$content']
        base = args['$base']
        target = args['$target']
        return {'$translation': '\n' + self.translate(content, self.__get_language(base), self.__get_language(target))}
