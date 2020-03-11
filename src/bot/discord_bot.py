import re

import discord
import asyncio
from src.bot.bot import Bot
from src.messages.discord_request import DiscordRequest
from src.messages.response import Response

MENTION_REGEX = r'<@\!\d+>'


class DiscordBot(Bot, discord.Client):
    client_id = None

    def __init__(self, token):
        Bot.__init__(self, token)
        asyncio.get_child_watcher()

        self.myloop = asyncio.get_event_loop()
        self.myloop.create_task(self.__start_loop())
        discord.Client.__init__(self, loop=self.myloop)

    async def __start_loop(self):
        await self.start(self.token)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    def is_direkt_message(self, message):
        return True if str(message.channel.type) == 'private' else False

    def is_mentioned(self, message):
        return self.user in message.mentions

    async def on_message(self, message):
        if message.author == self.user:
            return
        request = DiscordRequest(message)
        content = request.get_text()
        if self.is_direkt_message(message) or self.is_mentioned(message):
            content = re.sub(MENTION_REGEX, '', content).strip()
            plugin, method, params = self.handler.validate_user_input(content)
            answer = plugin.call_method(method, params)
            response = Response(answer, message)
            await self.send_message(response)

    async def send_message(self, response):
        await response.get_receiver().channel.send(response.get_message())

    def exit(self):
        self.myloop.stop()

    def start_bot(self, handler):
        self.handler = handler
        self.myloop.run_forever()
