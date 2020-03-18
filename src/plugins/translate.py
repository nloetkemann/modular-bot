from src.yaml.plugin import Plugin
from translate import Translator


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

    def translate_from_german(self, args):
        self.requiere_param(args, '$content', '$language')
        content = args['$content']
        language = args['$language']
        translator = Translator(from_lang='de', to_lang=self.__get_language(language))
        translation = translator.translate(content)
        return {'$translation': '\n' + translation}
