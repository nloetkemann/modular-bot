class TokenException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'Tokenexception: missing Token for {0}'.format(self.message)
        else:
            return 'Tokenexception: Error with a Token'
