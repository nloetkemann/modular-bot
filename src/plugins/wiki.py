from src.yaml.plugin import Plugin


class Wiki(Plugin):
    token_required = True

    def search_wiki(self, args):
        """
        performes a search at wiki
        :param args: the params in format {$searchKeyword: 'value'}
        :return: the result of the search
        """
        self.requiere_keyword_param(args, '$searchKeyword')
        search_keyword = args['$searchKeyword']

        print('Ich suche nach ' + search_keyword)
