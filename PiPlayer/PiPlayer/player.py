import mpd

class player(object):
    def __init__(self, host = 'localhost', port = 6600):
        self.name = None
        self.client = mpd.MPDClient()
        self.client.connect(host, port)
        self.volume = 100
        self.client.setvol(self.volume)

    def change_radio(self, url = None, name = None):
        if url is None or name is None:
            return
        self.name = name
        self.client.clear()
        self.client.add(url)
        self.client.play()

    def vol_up(self):
        if self.volume == 100:
            return
        self.volume += 25
        self.client.setvol(self.volume)

    def vol_down(self):
        if self.volume == 0:
            return
        self.volume -= 25
        self.client.setvol(self.volume)

    def pause(self):
        self.client.pause(1)

    def unpause(self):
        self.client.pause(0)