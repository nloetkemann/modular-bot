from src.messages.request import Request


class TelegramRequest(Request):
    def __init__(self, message_text):
        self.all = message_text
        self.user = message_text['from']['first_name']
        if 'chat' in message_text:
            self.chat_id = message_text['chat']['id']
        elif 'id' in message_text:
            self.chat_id = message_text['id']
        else:
            self.chat_id = ''

        if 'message' in message_text:
            if 'text' in message_text['message']:
                self.type = 'text'
            elif 'voice' in message_text['message']:
                self.type = 'voice'
            elif 'document' in message_text['message']:
                self.type = 'document'
            else:
                self.type = None
        else:
            if 'text' in message_text:
                self.type = 'text'
            elif 'voice' in message_text:
                self.type = 'voice'
            elif 'document' in message_text:
                self.type = 'document'
            else:
                self.type = None

        self.is_voice_file = self.is_voice()  # could be an document type but a voice message

    def get_text(self):
        if self.is_callback():
            return self.all['message']['text']
        elif self.is_text():
            return self.all['text']
        return None

    def is_callback(self):
        return 'message' in self.all

    def get_file_id(self):
        if self.is_voice():
            return self.all['voice']['file_id']
        elif self.is_document():
            return self.all['document']['file_id']

    def is_command(self):
        text = self.get_text()
        if text is not None:
            return text.find('/') == 0
        return False

    def get_attr(self, attribute, where=None):
        if where is None:
            if attribute in self.all:
                return self.all[attribute]
        else:
            if where in self.all:
                if attribute in self.all[where]:
                    return self.all[where][attribute]
        return None
