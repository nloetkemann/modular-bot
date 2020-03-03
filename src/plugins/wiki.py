from src.plugins.plugin import Plugin


class Wiki(Plugin):
    token_required = True

    def search_wiki(self, args):
        self.requiere_param(args, '$searchKeyword')
        search_keyword = args['$searchKeyword']

        print('Ich suche nach ' + search_keyword)
