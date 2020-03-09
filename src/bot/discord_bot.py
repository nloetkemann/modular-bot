import discord

from src.bot.bot import Bot


class DiscordBot(Bot, discord.Client):

    def __init__(self, token):
        super().__init__(token)
        client = DiscordBot()

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

    def send_message(self, response):
        pass

    def exit(self):
        pass

    def run(self, handler):
        self.run(self.token)



