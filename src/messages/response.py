class Response:
    def __init__(self, content, receiver, *args):
        self.message = content
        self.receiver = receiver
        self.args = args

    def get_message(self):
        return self.message

    def get_receiver(self):
        return self.receiver
