class Response:
    def __init__(self, content, receiver):
        self.message = content
        self.receiver = receiver

    def get_message(self):
        return self.message

    def get_receiver(self):
        return self.receiver
