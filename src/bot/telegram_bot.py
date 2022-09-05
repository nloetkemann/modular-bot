import logging
import telepot
from telepot.exception import TelegramError
from telepot.loop import MessageLoop
from src.bot.bot import Bot
from src.exceptions.not_found_exception import NotFoundException
from src.messages.response import Response
from src.messages.telegram_request import TelegramRequest
from src.plugin_handler import PluginHandler
from src.tools.tools import Tools

logger = logging.getLogger(__name__)


class TelegramBot(Bot):
    name = 'telegram'
    bold_regex = '*'
    bold_italic_regex = '`'
    italic_regex = '_'

    def __init__(self, token: str):
        super().__init__(token)
        self.bot = telepot.Bot(self.token)
        self.loop = None

    def start_bot(self, handler: PluginHandler):
        self.handler = handler
        try:
            MessageLoop(self.bot, {
                'chat': self.__on_chat_message,
                'callback_query': self.__on_chat_message
            }).run_forever()
        except Exception as e:
            logger.warning('Messageloop exited.')

    def exit(self):
        self.bot = None

    def send_message(self, response: Response):
        message = self.format_answer(response.get_message())
        if len(message) > 1000:
            shorter_message = Tools.split(message, 1000, '\n')
            rest_message = message[len(shorter_message):]
            self.bot.sendMessage(response.get_receiver(), shorter_message, parse_mode='MarkdownV2')
            response.message = rest_message
            self.send_message(response)
        else:
            self.bot.sendMessage(response.get_receiver(), message, parse_mode='MarkdownV2')

    def send_image(self, response: Response):
        with open(response.get_message(), 'rb') as file:
            self.bot.sendPhoto(response.get_receiver(), file)

    def __on_chat_message(self, message: str):
        request = TelegramRequest(message)
        plugin, method, params = self.handler.validate_user_input(request.get_text())
        params['chat_id'] = request.chat_id
        params['messenger'] = 'telegram'
        try:
            answer, file, _type = plugin.call_method(method, params)
            response = Response(answer, request.chat_id)
            try:
                self.send_message(response)
            except TelegramError as e:
                logger.error('Telegram Error', e)
                logger.error(response.get_message())
            if _type != '':
                if _type == 'photo':
                    self.send_image(Response(file, request.chat_id))
                Tools.remove_file(file)
        except NotFoundException as e:
            answer = e.message
            response = Response(answer, request.chat_id)
            self.send_message(response)


    def __on_callback(self, callback):
        print(callback)
