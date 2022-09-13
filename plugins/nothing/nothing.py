from src.yaml.plugin import Plugin


class Nothing(Plugin):

    def wrong_command(self, args):
        return {}
