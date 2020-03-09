from src.messages.request import Request


class DiscordRequest(Request):
    def get_text(self):
        pass

    def is_callback(self):
        pass

    def get_file_id(self):
        pass

    def is_command(self):
        pass

    def get_attr(self, attribute, where=None):
        pass
