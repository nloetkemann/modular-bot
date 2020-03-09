from src.yaml.plugin import Plugin


class Wolfram(Plugin):
    def add_numbers(self, args):
        print(args)

        return {'$result': 12}