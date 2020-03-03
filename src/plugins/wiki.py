from src.exceptions.token_exception import TokenException
from src.plugins.plugin import Plugin


class Wiki(Plugin):
    token_required = True

    def __init__(self, name, config):
        super().__init__(name, config)

    def search_wiki(self, args):
        print(self.token)
        print("wiki")
