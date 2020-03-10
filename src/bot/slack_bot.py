from src.bot.bot import Bot
from slackclient import SlackClient
import time
import re

DELAY = 1
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


class SlackBot(Bot):

    def __init__(self, token):
        super().__init__(token)
        self.slack_client = SlackClient(self.token)
        self.bot_id = self.slack_client.api_call("auth.test")["user_id"]

    def __parse_bot_commands(self, slack_events):
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                user_id, message = self.__parse_direct_mention(event["text"])
                if user_id == self.bot_id:
                    return message, event["channel"]
        return None, None

    def __parse_direct_mention(self, message_text):
        matches = re.search(MENTION_REGEX, message_text)
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def start_bot(self, handler):
        while True:
            command, channel = self.__parse_bot_commands(self.slack_client.rtm_read())
            if command:
                print(command)
                # handle_command(command, channel)
            time.sleep(DELAY)

    def send_message(self, response):
        pass

    def exit(self):
        pass
