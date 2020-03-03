from src.plugins.plugin import Plugin


class Wiki(Plugin):
    token_required = True

    def search_wiki(self, args):
        print(self.token)
        print("wiki")
