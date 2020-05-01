import mpd

test = mpd.MPDClient();
#test.connect("localhost",6600)
#test.clear()
test.add("http://example.com")
test.play()

class player(object):
    def __init__(self):
        self.dupa = 1