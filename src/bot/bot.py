import re


class Bot:
    token = ''
    name = ''
    bot = None
    retry = 0
    handler = None

    bold_regex = ''
    italic_regex = ''
    bold_italic_regex = ''

    def __init__(self, token):
        self.token = token

    def start_bot(self, handler):
        raise NotImplementedError('The run method has not been implemented ' + str(self.__class__))

    def send_message(self, response):
        raise NotImplementedError('The send_message method has not been implemented ' + str(self.__class__))

    def exit(self):
        raise NotImplementedError('The send_message method has not been implemented ' + str(self.__class__))

    def format_answer(self, answer):
        answer = re.sub(r'\*\*', self.bold_regex, answer)
        answer = re.sub(r'__', self.italic_regex, answer)
        answer = re.sub(r'\*_', self.bold_italic_regex, answer)
        return answer
