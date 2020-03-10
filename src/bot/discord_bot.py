import discord
import asyncio
from src.bot.bot import Bot
from src.messages.discord_request import DiscordRequest


class DiscordBot(Bot, discord.Client):

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

    async def on_message(self, message):
        if message.author == self.user:
            return
        request = DiscordRequest(message)
        plugin, method, params = self.handler.validate_user_input(request.get_text())
        answer = plugin.call_method(method, params)
        await message.channel.send(answer)

    async def send_message(self, response):
        pass

    def exit(self):
        pass

    def start_bot(self, handler):
        self.handler = handler
        self.myloop.run_forever()
