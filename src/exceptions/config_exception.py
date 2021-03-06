class ConfigException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Configexception: Error with the config: {0}'.format(self.message)
        else:
            return 'Configexception: Error with a the config'
