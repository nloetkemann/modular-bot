import logging
import re
import yamale
import os
import yaml

logger = logging.getLogger(__name__)


class Tools:
    @staticmethod
    def remove_regex(regex: str):
        """
        removes all regex chars
        :param regex: the regex
        :return: str
        """
        return re.sub(r'(\(|\)|\||\?)+', '', regex)

    @staticmethod
    def validate_yaml(schema_file: str, yaml_file: str):
        """
        checks if the yaml config file is valid
        :param schema_file: the path of the schema file
        :param yaml_file: the path of the yaml file
        :return: bool, ''
        """
        schema = yamale.make_schema(schema_file)
        data = yamale.make_data(yaml_file)
        try:
            yamale.validate(schema, data)
            logger.info('Yamlfiles is valid {0}'.format(yaml_file))
        except ValueError as e:
            logger.error('Yaml file is mal formated. ' + str(e))
            return False, 'Yaml file is mal formated. ' + str(e)
        return True, ''

    @staticmethod
    def read_config_file(path: str):
        """
        reads the config file and returns it
        :param path: the path of the config file
        :return: the configuration
        """
        if not os.path.isfile(path):
            raise FileNotFoundError('The config file is missing.')

        with open(path, 'r') as config_file:
            return yaml.load(config_file)

    @staticmethod
    def split(content: str, count: int = 600, needle: str = '.'):
        content_part = content[:count]
        sentences = content_part.split(needle)
        if len(sentences) > 2:
            sentences.pop()
            return needle.join(sentences)
        else:
            return needle.join(Tools.split(content, count + 100))

    @staticmethod
    def first_to_upper(word: str):
        return word[0].upper() + word[1:]
