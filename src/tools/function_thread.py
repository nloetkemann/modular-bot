from threading import Thread


class FunctionThread:
    def __init__(self, function, args=[]):
        self.function = function
        self.thread = Thread(target=self.function, args=args)

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.join()
