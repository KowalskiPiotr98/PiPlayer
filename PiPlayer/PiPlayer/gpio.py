from PiPlayer.player import Player, radio
from PiPlayer.station import Station, radios, radios_mutex
from threading import Thread
import gpiod
from time import sleep
from sys import argv, exit

B1_OFFSET=12
B2_OFFSET=13
B3_OFFSET=14
D1_OFFSET=24
D2_OFFSET=25
D3_OFFSET=26
D4_OFFSET=27
CHIP_NAME = '10008000.gpio'
SKIP_GPIO = False
BUILDROOT_GPIOD = False

def _print_usage():
    print ('USAGE: python3 runserver.py B1_OFFSET B2_OFFSET B3_OFFSET D1_OFFSET D2_OFFSET D3_OFFSET D4_OFFSET CHIP_NAME [--no-gpio] [--buildroot-gpiod]')
    exit (1)

for i in argv:
    if i == '--help' or i == '-h':
        _print_usage()

for i in argv:
    if i == '--no-gpio':
        SKIP_GPIO = True
        break

if len(argv) == 9 and not SKIP_GPIO:
    try:
        B1_OFFSET = int(argv [1])
        B2_OFFSET = int(argv [2])
        B3_OFFSET = int(argv [3])
        D1_OFFSET = int(argv [4])
        D2_OFFSET = int(argv [5])
        D3_OFFSET = int(argv [6])
        D4_OFFSET = int(argv [7])
        CHIP_NAME = argv [8]
    except ValueError:
        _print_usage()

elif len(argv) != 1 and not SKIP_GPIO:
    _print_usage()
if not SKIP_GPIO:
    if BUILDROOT_GPIOD:
        _chip = gpiod.Chip(CHIP_NAME)
    else:
        _chip = gpiod.chip(CHIP_NAME)
    _b1 = _chip.get_line(B1_OFFSET)
    _b2 = _chip.get_line(B2_OFFSET)
    _b3 = _chip.get_line(B3_OFFSET)
    _d1 = _chip.get_line(D1_OFFSET)
    _d1.request(consumer='PiPlayer', type=gpiod.LINE_REQ_DIR_OUT)
    _d1.set_value(1)
    _d2 = _chip.get_line(D2_OFFSET)
    _d2.request(consumer='PiPlayer', type=gpiod.LINE_REQ_DIR_OUT)
    _d2.set_value(1)
    _d3 = _chip.get_line(D3_OFFSET)
    _d3.request(consumer='PiPlayer', type=gpiod.LINE_REQ_DIR_OUT)
    _d3.set_value(0)
    _d4 = _chip.get_line(D4_OFFSET)
    _d4.request(consumer='PiPlayer', type=gpiod.LINE_REQ_DIR_OUT)
    _d4.set_value(0)

    _state = 0 #0 - playback, 1 - selection, 2 - volume change, -1 - finish

def gpio_thread(arg):
    global _state
    while _state != -1:
        if BUILDROOT_GPIOD:
            bulk_event = gpiod.LineBulk([_b1, _b2, _b3])
        else:
            bulk_event = gpiod.line_bulk([_b1, _b2, _b3])
        bulk_event.request(consumer='PiPlayer', type=gpiod.LINE_REQ_EV_FALLING_EDGE)
        events = bulk_event.event_wait(sec = 2)
        if events is not None:
            button = events[0]
            sleep(0.5)
            if button.get_value() == 1:
                offset = button.offset()
                if _state == 0:
                    _handle_playback(offset)
                elif _state == 1:
                    _handle_selection(offset)
                elif _state == 2:
                    _handle_volume(offset)
        bulk_event.release()

def _handle_volume(offset):
    global _state
    _set_volume_leds()
    if offset == B1_OFFSET:
        radio.vol_down()
        _set_volume_leds()
    elif offset == B2_OFFSET:
        radio.vol_up()
        _set_volume_leds()
    elif offset == B3_OFFSET:
        _d1.set_value(1)
        if radio.get_is_playing():
            _d2.set_value(0)
        else:
            _d2.set_value(1)
        _d3.set_value(0)
        _d4.set_value(0)
        _state = 0
    
def refresh_playback_leds():
    if SKIP_GPIO:
        return
    _d3.set_value(0)
    _d4.set_value(0)
    _d1.set_value(1)
    if radio.get_is_playing():
        _d2.set_value(0)
    else:
        _d2.set_value(1)

def _set_volume_leds():
    _d1.set_value(0)
    _d2.set_value(0)
    _d3.set_value(0)
    _d4.set_value(0)
    vol = radio.get_volume()
    if vol > 0:
        _d1.set_value(1)
    if vol > 25:
        _d2.set_value(1)
    if vol > 50:
        _d3.set_value(1)
    if vol > 75:
        _d4.set_value(1)

def _handle_selection(offset):
    global _state
    if offset == B1_OFFSET: #prev
        if len(radios) == 0:
            return
        name = radio.get_name()
        with radios_mutex:
            if len(radios) == 1 or radios[0].name == name:
                temp = radios[len(radios) - 1]
                radio.change_radio (temp.url, temp.name)
                return
            for i in range(1, len(radios)):
                if radios[i].name == name:
                    radio.change_radio (radios [i-1].url, radios [i-1].name)
                    return
            radio.change_radio (radios [0].url, radios [0].name)
    elif offset == B2_OFFSET: #next
        if len(radios) == 0:
            return
        name = radio.get_name()
        with radios_mutex:
            if len(radios) == 1 or radios[len(radios) - 1].name == name:
                temp = radios[0]
                radio.change_radio (temp.url, temp.name)
                return
            for i in range(0, len(radios) - 1):
                if radios[i].name == name:
                    radio.change_radio (radios [i+1].url, radios [i+1].name)
                    return
            radio.change_radio (radios [0].url, radios [0].name)
    elif offset == B3_OFFSET: #confirm
        _state = 0
        _d1.set_value(1)
        _d2.set_value(0)
        _d3.set_value(0)

def _handle_playback(offset):
    global _state
    if offset == B1_OFFSET:
        _d1.set_value(1)
        if len(radios) == 0:
            _d2.set_value(1)
        elif radio.get_is_playing():
            radio.pause()
            _d2.set_value(1)
        elif radio.get_name() is None:
            with radios_mutex:
                radio.change_radio(radios[0].url, radios[0].name)
            _d2.set_value(0)
        else:
            radio.unpause()
            _d2.set_value(0)
    elif offset == B2_OFFSET:
        _state = 1
        _d1.set_value(0)
        _d2.set_value(0)
        _d3.set_value(1)
    elif offset == B3_OFFSET:
        _state = 2
        _set_volume_leds()

if not SKIP_GPIO:
    _thread = Thread(target = gpio_thread, args = ('',))
    _thread.start()

def thread_join():
    if SKIP_GPIO:
        return
    global _state
    _state = -1
    _thread.join()
    _d1.set_value(0)
    _d1.release()
    _d2.set_value(0)
    _d2.release()
    _d3.set_value(0)
    _d3.release()
    _d4.set_value(0)
    _d4.release()
