from PiPlayer.player import Player, radio
from PiPlayer.station import Station, radios
from threading import Thread
import gpiod

_chip = gpiod.Chip('10008000.gpio')
_b1 = _chip.get_line(12)
_b2 = _chip.get_line(13)
_b3 = _chip.get_line(14)
_d1 = _chip.get_line(24)
_d1.request(consumer='PiPlayer', type=gpiod.LINE_REQ_DIR_OUT)
_d2 = _chip.get_line(25)
_d2.request(consumer='PiPlayer', type=gpiod.LINE_REQ_DIR_OUT)
_d3 = _chip.get_line(26)
_d3.request(consumer='PiPlayer', type=gpiod.LINE_REQ_DIR_OUT)
_d4 = _chip.get_line(27)
_d4.request(consumer='PiPlayer', type=gpiod.LINE_REQ_DIR_OUT)

_state = 0 #0 - playback, 1 - selection, 2 - volume change, -1 - finish

def gpio_thread(arg):
    while _state != -1:
        _d1.set_value(1)
        bulk_event = gpiod.line_bulk([_b1, _b2, _b3])
        bulk_event.request(consumer='PiPlayer', type=gpiod.LINE_REQ_EV_BOTH_EDGES)
        events = bulk_event.event_wait(sec = 2)
        if events.size > 0:
            for i in events:
                print(i)
        bulk_event.release()
        _d1.set_value(0)

_thread = Thread(target = gpio_thread, args = ('',))
_thread.start()

def thread_join():
    _state = -1
    _thread.join()
    _d1.release()
    _d2.release()
    _d3.release()
    _d4.release()
