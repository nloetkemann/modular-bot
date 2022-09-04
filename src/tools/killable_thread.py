from threading import Thread


class KillableThread(Thread):
    _target = None
    _args = None
    running = False
    value = None
    name: str

    def __init__(self, function=None, name='', args=[]):
        self.arguments = args
        Thread.__init__(self, target=function, args=(self, *args))
        self.name = name

    def run(self):
        self.running = True
        super(KillableThread, self).run()

    def stop(self):
        self.running = False
