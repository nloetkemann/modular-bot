from src.messages.request import Request


class SlackRequest(Request):
    def __init__(self, content):
        self.chat_id = content['channel']
        self.user = content['user']

    def get_text(self):
        pass
