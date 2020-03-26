from threading import Thread


class MethodThread(Thread):
    _target = None
    _args = None

    def __init__(self, function=None, *args):
        print(args)
        self.arguments = args
        Thread.__init__(self, target=function, args=args)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self.arguments)

    def join_get_response(self, *args):
        Thread.join(self, *args)
        return self._return
