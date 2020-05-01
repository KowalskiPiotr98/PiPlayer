import mpd

class player(object):
    def __init__(self, host = 'localhost', port = 6600):
        self.name = None
        self._host = host
        self._port = port
        self.client = mpd.MPDClient()
        self.client.connect(host, port)
        self.client.stop()
        self.volume = 100
        self.playing = False
        self.client.setvol(self.volume)
        self.client.disconnect()

    def change_radio(self, url = None, name = None):
        if url is None or name is None:
            return
        self.client.connect(self._host, self._port)
        self.playing = True
        self.name = name
        self.client.clear()
        self.client.add(url)
        self.client.play()
        self.client.disconnect()

    def vol_up(self):
        if self.volume == 100:
            return
        self.volume += 25
        self.client.connect(self._host, self._port)
        self.client.setvol(self.volume)
        self.client.disconnect()

    def vol_down(self):
        if self.volume == 0:
            return
        self.volume -= 25
        self.client.connect(self._host, self._port)
        self.client.setvol(self.volume)
        self.client.disconnect()

    def pause(self):
        self.client.connect(self._host, self._port)
        self.client.pause(1)
        self.client.disconnect()
        self.playing = False

    def unpause(self):
        self.client.connect(self._host, self._port)
        self.client.pause(0)
        self.client.disconnect()
        self.playing = True