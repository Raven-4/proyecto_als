import flask
import flask_login
import sirope
from flask import render_template, redirect, url_for, request
import uuid

from model.song import Song
from model.user import User
from model.favoriteSong import FavoriteSong

def get_song_blueprint():
    song_bp = flask.Blueprint('songs', __name__, url_prefix="/songs", template_folder="templates", static_folder="static")
    srp = sirope.Sirope()
    return song_bp, srp

song_bp, srp = get_song_blueprint()

@song_bp.route("/show_songs", methods=["GET", "POST"])
@flask_login.login_required
def show_songs():
    usr = User.current_user()
    songs = list(srp.load_all(Song))

    songs_data = []
    for song in songs:
        song_dict = {
            "id": song.identificador,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre
        }
        songs_data.append(song_dict)

    print(songs_data)
    sust = {
        "usr": usr,
        "songs_data": songs_data
    }

    return render_template("show_songs.html", **sust)

@song_bp.route("/add_song", methods=["GET", "POST"])
@flask_login.login_required
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
        
        song = Song(id = str(uuid.uuid4()), title=title, artist=artist, genre=genre)

        song_oid = srp.save(song)

        usr.add_song_oid(song_oid)  
        srp.save(usr)

        return flask.redirect(url_for("songs.show_songs"))
    
    return render_template("add_song.html", usr=usr)

@song_bp.route("/search_songs", methods=["GET", "POST"])
@flask_login.login_required
def search_songs():
    usr = User.current_user()
    if request.method == "POST":
        search_query = request.form.get("search_query")
        filter_criteria = request.form.get("filter_criteria")
        
        if filter_criteria == "all":
            filtered_songs = [song for song in srp.load_all(Song) if 
                              search_query.lower() in song.title.lower() 
                              or search_query.lower() in song.artist.lower() 
                              or search_query.lower() in song.genre.lower()]
        else:
            filtered_songs = [song for song in srp.load_all(Song) if 
                              search_query.lower() in getattr(song, filter_criteria).lower()]

        sust = {
            "usr": usr,
            "songs": filtered_songs,
            "search_query": search_query
        }
        return render_template("show_songs.html", **sust)
    return redirect(url_for("songs.show_songs"))

@song_bp.route("/favorite_song", methods=["POST"])
@flask_login.login_required
def favorite_song():
    usr = User.current_user()
    song_id = request.form.get("song_id")  # Obtener el ID de la canción desde el formulario
    songs = list(srp.load_all(Song))

    if usr and song_id is not None:
        song = next((song for song in songs if song.id == song_id), None)

        if song:
            favorite = FavoriteSong(username=usr.username, song_data=song)
            srp.save(favorite)
            flask.flash(f"{song.title} marcada como favorita.")
        else:
            flask.flash("Canción no encontrada.")
    else:
        flask.flash("Usuario no encontrado o ID de canción no proporcionado.")

    return flask.redirect(flask.url_for("songs.show_songs"))

@song_bp.route("/show_favorites", methods=["POST"])
@flask_login.login_required
def show_favorites():
    usr = User.current_user()
    if usr:
        favorite_songs = [favorite.song_data for favorite in usr.favorite_songs]
        sust = {
            "usr": usr,
            "songs_data": favorite_songs
        }
        return render_template("show_songs.html", **sust)
    else:
        flask.flash("Debes iniciar sesión para ver tus favoritos.")
        return redirect(url_for("index"))
