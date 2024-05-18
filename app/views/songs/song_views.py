import flask
import sirope
from flask import render_template, redirect, url_for, request

from model.song import Song
from model.user import User

def get_song_blueprint():
    song_bp = flask.Blueprint('songs', __name__, url_prefix="/songs", template_folder="templates", static_folder="static")
    srp = sirope.Sirope()
    return song_bp, srp

song_bp, srp = get_song_blueprint()

@song_bp.route("/show_songs", methods=["GET", "POST"])
def show_songs():
    usr = User.current_user()
    songs = list(srp.load_all(Song))

    sust = {
        "usr": usr,
        "songs": songs
    }

    return render_template("show_songs.html", **sust)

@song_bp.route("/add_song", methods=["GET", "POST"])
def add_song():
    usr = User.current_user()

    if request.method == "POST":
        title = request.form.get("title")
        artist = request.form.get("artist")
        genre = request.form.get("genre")
        
        if not title:
            flask.flash("¿Y el título?")
            return flask.redirect(url_for("song.add_song"))
        
        if not artist:
            flask.flash("¿Y el artista?")
            return flask.redirect(url_for("song.add_song"))
        
        if not genre:
            flask.flash("¿Y el género?")
            return flask.redirect(url_for("song.add_song"))
        
        song = Song(title=title, artist=artist, genre=genre)
        song_oid = srp.save(song)

        usr.add_song_oid(song_oid)  
        srp.save(usr)

        return flask.redirect(url_for("songs.show_songs"))
    
    return render_template("add_song.html", usr=usr)
