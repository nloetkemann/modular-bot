from src.yaml.plugin import Plugin


class Health(Plugin):
    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)

    def feel_sick(self, args):
        print(args)
        return {'$result': 'test'}
