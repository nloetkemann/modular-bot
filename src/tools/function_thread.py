from threading import Thread


class FunctionThread:
    def __init__(self, function, args=[]):
        self.function = function
        self.stop_thread = False
        self.thread = Thread(target=self.function, args=args)

    def start(self):
        self.thread.start()

    # def stop(self):
    #     self.stop_thread = True
    #     self.thread.join()
