"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import *
from PiPlayer import app
from PiPlayer.station import *

radios = [station ("BBC one", "https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_one.mpd"),
          station ("Złote przeboje", "http://stream10.radioagora.pl/zp_waw_128.mp3")]

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/stations')
def stations():
    return render_template(
        'stations.html',
        title='Stations',
        year=datetime.now().year,
        stations = radios,
    )

@app.route('/changeUrl', methods=['POST'])
def changeUrl(name):
    return redirect('/stations')

@app.route('/radioUp', methods=['POST'])
def radioUp():
    name = request.form.get('name')
    if name is None:
        return redirect('/stations')
    for i in range(0,len(radios)):
        if radios [i].name == name:
            if i > 0:
                temp = radios [i]
                radios [i] = radios [i-1]
                radios [i - 1] = temp
            break
    return redirect('/stations')

@app.route('/radioDown', methods=['POST'])
def radioDown():
    name = request.form.get('name')
    if name is None:
        return redirect('/stations')
    for i in range(0,len(radios)):
        if radios [i].name == name:
            if i < len(radios) - 1:
                temp = radios [i]
                radios [i] = radios [i + 1]
                radios [i + 1] = temp
            break
    return redirect('/stations')