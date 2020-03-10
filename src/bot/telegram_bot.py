import logging

import telepot
from telepot.loop import MessageLoop

from src.bot.bot import Bot
from src.messages.response import Response
from src.messages.telegram_request import TelegramRequest
from src.plugin_handler import PluginHandler

logger = logging.getLogger(__name__)


class TelegramBot(Bot):
    name = 'telegram'

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
        return self.bot.sendMessage(response.get_receiver(), response.get_message(), parse_mode='Markdown')

    def __on_chat_message(self, message: str):
        request = TelegramRequest(message)
        plugin, method, params = self.handler.validate_user_input(request.get_text())
        answer = plugin.call_method(method, params)
        response = Response(answer, request.chat_id)
        self.send_message(response)

    def __on_callback(self, callback):
        print(callback)
