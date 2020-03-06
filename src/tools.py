import re


class Tools:
    @staticmethod
    def remove_regex(regex):
        """
        removes all regex chars
        :param regex: the regex
        :return: str
        """
        return re.sub(r'(\(|\)|\||\?)+', '', regex)
