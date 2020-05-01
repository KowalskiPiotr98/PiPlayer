"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect
from PiPlayer import app
from PiPlayer.station import *
from PiPlayer.player import *

radios = [station ("BBC one", "https://a.files.bbci.co.uk/media/live/manifesto/audio/simulcast/dash/nonuk/dash_low/llnws/bbc_radio_one.mpd"),
          station ("Złote przeboje", "http://stream10.radioagora.pl/zp_waw_128.mp3")]
radio = player()

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

@app.route('/radioUp', methods=['POST'])
def radio_up():
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
def radio_down():
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

@app.route('/edit/<name>')
def edit(name):
    if name is None:
        return redirect('/stations')
    for i in radios:
        if name == i.name:
            return render_template(
                'edit.html',
                title="Edit",
                year=datetime.now().year,
                station = i,
                )
    return redirect('/stations')

@app.route('/edit/<name>', methods=['POST'])
def edit_post(name):
    if name is None:
        return redirect('/stations')
    for i in radios:
        if i.name == name:
            i.url = request.form.get('url')
            break
    return redirect('/stations')

@app.route('/delete', methods=['POST'])
def edit_delete():
    name = request.form.get('name')
    if name is None:
        return redirect('/stations')
    for i in radios:
        if i.name == name:
            radios.remove(i)
            break
    return redirect('/stations')

@app.route('/newStation')
def new_station():
    return render_template(
        'new_station.html',
        title = 'New station',
        year = datetime.now().year
        )

@app.route('/newStation', methods = ['POST'])
def new_station_post():
    name = request.form.get('name')
    url = request.form.get('url')
    if name is None or url is None or name == '' or url == '':
        return redirect('/newStation')
    for i in radios:
        if i.name == name:
            return redirect('/newStation')
    radios.append(station(name, url))
    return redirect('/stations')

@app.route('/api/name')
def api_name():
    return radio.name, 200

@app.route('/api/next', methods=['POST'])
def api_next():
    if len(radios) == 0:
        return '', 400
    if len(radios) == 1 or radios[len(radios) - 1].name == radio.name:
        radio.change_radio (radios [0].url, radios [0].name)
        return radio.name, 200
    for i in range(0,len(radios) - 1):
        if radios [i].name == radio.name:
            radio.change_radio (radios [i+1].url, radios [i+1].name)
            return radio.name, 200
    radio.change_radio (radios [0].url, radios [0].name)
    return radio.name, 200

@app.route('/api/prev', methods=['POST'])
def api_prev():
    if len(radios) == 0:
        return '', 400
    if len(radios) == 1 or radios[0].name == radio.name:
        rTemp = radios[len(radios) - 1]
        radio.change_radio (rTemp.url, rTemp.name)
        return radio.name, 200
    for i in range(1, len(radios)):
        if radios [i].name == radio.name:
            radio.change_radio (radios [i-1].url, radios [i-1].name)
            return radio.name, 200
        radio.change_radio(radios [0].url, radios [0].name)
    return radio.name, 200

@app.route('/api/pause', methods=['POST'])
def api_pause():
    radio.pause()
    return '', 200

@app.route('/api/unpause', methods=['POST'])
def api_unpause():
    if len(radios) == 0:
        return '', 200
    if radio.name is None:
        radio.change_radio (radios [0].url, radios[0].name)
    else:
        radio.unpause()
    return '', 200

@app.route('/api/volume/<change>', methods=['POST'])
def api_volume(change = None):
    if change is None:
        return 400
    if change == 'up':
        radio.vol_up()
    elif change == 'down':
        radio.vol_down()
    else:
        return 400
    return str(radio.volume), 200

@app.route('/api/isplaying')
def api_is_playing():
    if radio.playing:
        return "yes", 200
    else:
        return "no", 200

@app.route('/api/getvolume')
def api_get_volume():
    return str(radio.volume), 200