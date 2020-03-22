class WrongNameException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'WrongNameException: Error with this name: {0}'.format(self.message)
        else:
            return 'WrongNameException: Error with the given name'
