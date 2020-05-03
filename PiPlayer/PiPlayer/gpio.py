from PiPlayer.player import Player, radio
from PiPlayer.station import Station, radios
from threading import Thread
import gpiod

_chip = gpiod.Chip('10008000.gpio')

def gpio_thread(arg):
    print('Start thread')
    button = _chip.get_line(13)
    button.request(consumer='PiPlayer', type=gpiod.LINE_REQ_EV_BOTH_EDGES)
    line = button.event_wait()
    if line:
        event = button.event_read()
        print(event)

_thread = Thread(target = gpio_thread, args = ('',))
_thread.start()

def thread_join():
    _thread.join()