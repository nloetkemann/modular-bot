from src.messages.request import Request


class DiscordRequest(Request):
    def __init__(self, message):
        self.text = message.content
        self.user = message.author
        self.chat_id = message

    def get_text(self):
        return self.text

    def is_callback(self):
        pass

    def get_file_id(self):
        pass

    def is_command(self):
        pass

    def get_attr(self, attribute, where=None):
        pass
