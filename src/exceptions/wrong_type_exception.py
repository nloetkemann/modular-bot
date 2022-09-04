class WrongTypeException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'WrongTypeException: Error with this parameter: {0}'.format(self.message)
        else:
            return 'WrongTypeException: Error with the given parameter'
