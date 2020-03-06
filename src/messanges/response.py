class Response:
    def __init__(self, content, receiver):
        self.message = 'Hallo'
        self.receiver = 'Nikita'

    def get_message(self):
        return self.message

    def get_receiver(self):
        return self.receiver
