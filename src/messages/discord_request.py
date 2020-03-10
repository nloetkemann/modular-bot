from src.messages.request import Request


class DiscordRequest(Request):
    def __init__(self, message):
        self.text = message.content
        self.user = message.author
        self.chat_id = message

    def get_text(self):
        return self.text
