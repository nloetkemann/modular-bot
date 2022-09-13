import asyncio

from src.client.client import Bot
from slack import RTMClient
from src.messages.response import Response
from src.messages.slack_request import SlackRequest

DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


class SlackBot(Bot):

    def __init__(self, token):
        super().__init__(token)
        print(token)
        asyncio.get_child_watcher()
        self.myloop = asyncio.get_event_loop()
        self.slack_client = RTMClient(token=str(self.token), loop=self.myloop)

    def __start_loop(self):
        future = asyncio.ensure_future(self.slack_client._connect_and_read(), loop=self.myloop)
        return self.myloop.run_until_complete(future)

    @RTMClient.run_on(event='message')
    def __handle_command(self, **payload):
        data = payload['data']
        print(data)
        request = SlackRequest(payload)
        response = Response('Hallo', request.chat_id, payload['rtm_client'])
        self.send_message(response)

    def send_message(self, response: Response):
        if len(response.args) == 1:
            response.args[0].chat_postMessage(
                channel=response.get_receiver(),
                text=response.get_message()
            )

    def send_image(self, response: Response):
        pass

    def start_bot(self, handler):
        self.handler = handler
        self.__start_loop()

    def exit(self):
        self.myloop.stop()
