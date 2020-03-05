from src.yaml.plugin import Plugin


class Welcome(Plugin):

    def say_hello(self, args):
        print("hi")

    def how_are_you(self, args):
        print('fine')
