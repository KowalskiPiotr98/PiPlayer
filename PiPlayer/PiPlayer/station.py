
class Station(object):
    def __init__(self, name, url):
        self.url = url
        self.name = name


radios = [Station ("BBC one", "https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_one.mpd"),
          Station ("Złote przeboje", "http://stream10.radioagora.pl/zp_waw_128.mp3")]