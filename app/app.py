import flask
import sirope
from flask import render_template, redirect, url_for, request
from app.models import Song
from app.forms import SongForm
from app import db

app = flask.Flask(__name__)
srp = sirope.Sirope()

@app.route('/')
def index():
    songs = Song.query.all()
    return render_template('index.html', songs=songs)

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        song = Song(title=form.title.data, artist=form.artist.data, genre=form.genre.data)
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_song.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)
