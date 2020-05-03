import mpd
import threading

mpc_mutex = threading.Lock()

class Player(object):
    def __init__(self, host = 'localhost', port = 6600):
        self._host = host
        self._port = port
        self.client = mpd.MPDClient()
        with mpc_mutex:
            self._name = None
            self.client.connect(host, port)
            self.client.stop()
            self._volume = 100
            self._playing = False
            self.client.setvol(self._volume)
            self.client.disconnect()

    def change_radio(self, url = None, name = None):
        if url is None or name is None:
            return
        with mpc_mutex:
            self._playing = True
            self._name = name
            self.client.connect(self._host, self._port)
            self.client.stop()
            self.client.clear()
            self.client.add(url)
            self.client.play()
            self.client.disconnect()

    def vol_up(self):
        if self._volume == 100:
            return
        with mpc_mutex:
            self._volume += 25
            self.client.connect(self._host, self._port)
            self.client.setvol(self._volume)
            self.client.disconnect()

    def vol_down(self):
        if self._volume == 0:
            return
        with mpc_mutex:
            self._volume -= 25
            self.client.connect(self._host, self._port)
            self.client.setvol(self._volume)
            self.client.disconnect()

    def pause(self):
        with mpc_mutex:
            self.client.connect(self._host, self._port)
            self.client.stop()
            self.client.disconnect()
            self._playing = False

    def unpause(self):
        with mpc_mutex:
            self.client.connect(self._host, self._port)
            self.client.play()
            self.client.disconnect()
            self._playing = True

    def get_volume(self):
        with mpc_mutex:
            temp = self._volume
        return temp

    def get_name(self):
        with mpc_mutex:
            temp = self._name
        return temp

    def set_name(self, name):
        with mpc_mutex:
            self._name = name
    
    def get_is_playing(self):
        with mpc_mutex:
            return self._playing

radio = Player()