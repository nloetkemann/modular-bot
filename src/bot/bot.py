class Bot:
    token = ''
    name = ''
    bot = None
    retry = 0
    handler = None

    def __init__(self, token):
        self.token = token

    def run(self, handler):
        raise NotImplementedError('The run method has not been implemented ' + str(self.__class__))

    def send_message(self, response):
        raise NotImplementedError('The send_message method has not been implemented ' + str(self.__class__))
