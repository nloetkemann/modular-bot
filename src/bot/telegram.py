import telepot
from requests import Response
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from src.bot.bot import Bot


class Telegram(Bot):
    name = 'telegram'

    def __init__(self, token):
        super().__init__(token)
        self.bot = telepot.Bot(self.token)

    def send_message(self, response):
        pass
        assert isinstance(response, Response)
        try:
            self.retry = 0
            return self.bot.sendMessage(response.origin_message.chat_id, response.text, reply_markup=keyboard)
        except ProtocolError as e:
            if self.retry == 0:
                self.send_message(response, keyboard)
                self.retry = 1
            else:
                self.retry = 0
                raise e

    def send_question(self, response):
        pass
        # return self.send_message(response, self._get_inline__keyboard(response.get_args()))

    def send_message_with_keyboard(self, response):
        pass
        # return self.send_message(response, self._get_custom_keyboard(response.get_args()))

    #  values should be dict
    def _get_inline__keyboard(self, values):
        pass
        # assert isinstance(values, dict)
        # all_keyboard = []
        # for key in values.keys():
        #     all_keyboard.append(InlineKeyboardButton(text=key, callback_data=values[key]))
        # keyboard = InlineKeyboardMarkup(inline_keyboard=[
        #     all_keyboard,
        # ])
        # return keyboard

    # values should be array
    def _get_custom_keyboard(self, values):
        pass
        # assert isinstance(values, list)
        # keyboard = ReplyKeyboardMarkup(keyboard=values, one_time_keyboard=True, resize_keyboard=True)
        # return keyboard

    def download_file(self, file_id, path):
        pass
        # self.bot.download_file(file_id, path)

    def answer_callback(self, query_id, text):
        pass
        # return self.bot.answerCallbackQuery(query_id, text)

    def edit_message(self, message_id, text):
        pass
        # return self.bot.editMessageText(message_id, text, reply_markup=None)

    def get_message_identifier(self, message):
        pass
        # return telepot.message_identifier(message)

    def delete_message(self, message_id):
        pass
        # self.bot.deleteMessage(message_id)

    def restart(self):
        pass
        # self.bot = telepot.Bot(os.environ['BOT_TOKEN'])
