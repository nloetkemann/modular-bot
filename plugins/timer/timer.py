from src.exceptions.not_found_exception import NotFoundException
from src.exceptions.wrong_type_exception import WrongTypeException
from src.tools.killable_thread import KillableThread
from src.yaml.plugin import Plugin
from src.config import config as global_config
import time


class Timer(Plugin):
    timer_list: {}
    multiplier = {'en': {'second': 1, 'seconds': 1, 'minute': 60, 'minutes': 60, 'hour': 360, 'hours': 360,
                         'day': 8640, 'days': 8640},
                  'de': {'sekunde': 1, 'sekunden': 1, 'minute': 60, 'minuten': 60, 'stunde': 360, 'stunden': 360,
                         'tag': 8640, 'tage': 8640}}

    def __init__(self, name, plugin_config):
        super().__init__(name, plugin_config)
        self.timer_list = {}

    @staticmethod
    def _run(thread, messenger, chat_id, seconds):
        thread.value = seconds
        while thread.running and thread.value > 0:
            time.sleep(1.)
            thread.value -= 1
        if thread.value == 0:
            global_config.message_trigger(messenger, chat_id, f'Der {thread.name} Timer ist vorbei')
        else:
            print('abort')
        return

    def _start_timer(self, messenger, chat_id, seconds, name):
        thread = KillableThread(function=self._run, name=name, args=(messenger, chat_id, seconds,))
        key = f'{messenger}_{chat_id}_{seconds}'
        self.timer_list[key] = thread
        thread.start()

    def _stop_timer(self, messenger, chat_id, seconds):
        key = f'{messenger}_{chat_id}_{seconds}'
        if key in self.timer_list:
            thread = self.timer_list[key]
            thread.stop()
            thread.join()
            self.timer_list.pop(key)
            return
        raise NotFoundException('No Timer found')

    def _status(self, messenger, chat_id, seconds):
        key = f'{messenger}_{chat_id}_{seconds}'
        if key in self.timer_list:
            return self.timer_list[key].value
        raise NotFoundException('No Timer found')

    def _cast(self, amount):
        try:
            return int(amount)
        except Exception:
            raise WrongTypeException('Not the correct param type: ' + amount)

    def _convert(self, seconds):
        days = int(seconds / 3640)
        seconds = seconds % 3640
        hours = int(seconds / 360)
        seconds = seconds % 360
        minute = int(seconds / 60)
        seconds = seconds % 60
        return days, hours, minute, seconds

    def set_timer(self, args):
        self.requiere_param(args, '$amount', '$timeunit')
        amount = self._cast(args['$amount'])
        unit = args['$timeunit']
        seconds = amount * self.multiplier[global_config.language][unit]
        self._start_timer(args['messenger'], args['chat_id'], seconds, f'{str(amount)} {unit}')
        return {}

    def stop_timer(self, args):
        self.requiere_param(args, '$amount', '$timeunit')
        amount = self._cast(args['$amount'])
        unit = args['$timeunit']
        seconds = amount * self.multiplier[global_config.language][unit]
        self._stop_timer(args['messenger'], args['chat_id'], seconds)
        return {}

    def status_timer(self, args):
        self.requiere_param(args, '$amount', '$timeunit')
        amount = self._cast(args['$amount'])
        unit = args['$timeunit']
        seconds = amount * self.multiplier[global_config.language][unit]
        try:
            rest_timer = self._status(args['messenger'], args['chat_id'], seconds)
        except NotFoundException as e:
            raise e
        days, hours, minutes, seconds = self._convert(rest_timer)
        timer = ''
        if days > 0:
            timer += f'{days} Tage '
        if hours > 0:
            timer += f'{hours} Stunden '
        if minutes > 0:
            timer += f'{minutes} Minuten '
        if seconds > 0:
            timer += f'{seconds} Sekunden '
        return {'$rest_timer': timer.strip()}

    def __del__(self):
        for timer in self.timer_list:
            timer.stop()
            timer.join()
