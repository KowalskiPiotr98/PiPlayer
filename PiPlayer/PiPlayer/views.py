"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect
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