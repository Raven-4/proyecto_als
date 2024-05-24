import flask
import flask_login
import sirope
from flask import render_template, redirect, url_for, request
import uuid

from model.song import Song
from model.user import User

def get_song_blueprint():
    song_bp = flask.Blueprint('songs', __name__, url_prefix="/songs", template_folder="templates", static_folder="static")
    srp = sirope.Sirope()
    return song_bp, srp

song_bp, srp = get_song_blueprint()

@song_bp.route("/toggle_view", methods=["POST"])
@flask_login.login_required
def toggle_view():
    usr = User.current_user()
    session = flask.session

    # Alterna el estado de la vista
    showing_favorites = session.get('showing_favorites', False)
    session['showing_favorites'] = not showing_favorites

    return flask.redirect(flask.url_for("songs.show_songs"))

@song_bp.route("/show_songs", methods=["GET", "POST"])
@flask_login.login_required
def show_songs():
    usr = User.current_user()
    songs = list(srp.load_all(Song))
    showing_favorites = flask.session.get('showing_favorites', False)

    if showing_favorites:
        songs = [song for song in songs if song.id in usr.favorite_songs_ids]

    songs_data = []
    for song in songs:
        song_dict = {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre,
            "comments": song.comments
        }
        songs_data.append(song_dict)

    print(songs_data)
    sust = {
        "usr": usr,
        "songs_data": songs_data,
        "showing_favorites": showing_favorites
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

        srp.save(song)
        song_oid = song.id
        usr.add_song_oid(song_oid)  
        srp.save(usr)

        return flask.redirect(url_for("songs.show_songs"))
    
    return render_template("add_song.html", usr=usr)

@song_bp.route("/search_songs", methods=["GET", "POST"])
@flask_login.login_required
def search_songs():
    usr = User.current_user()
    showing_favorites = flask.session.get('showing_favorites', False)
    
    if request.method == "POST":
        search_query = request.form.get("search_query")
        filter_criteria = request.form.get("filter_criteria")
        
        # Cargar las canciones de acuerdo al estado de favoritos
        if showing_favorites:
            songs = [song for song in srp.load_all(Song) if song.id in usr.favorite_songs_ids]
        else:
            songs = list(srp.load_all(Song))
        
        # Filtrar las canciones según la búsqueda
        if filter_criteria == "all":
            filtered_songs = [song for song in songs if 
                              search_query.lower() in song.title.lower() 
                              or search_query.lower() in song.artist.lower() 
                              or search_query.lower() in song.genre.lower()]
        else:
            filtered_songs = [song for song in songs if 
                              search_query.lower() in getattr(song, filter_criteria).lower()]

        filtered_songs_data = [
            {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "genre": song.genre
            } for song in filtered_songs
        ]

        sust = {
            "usr": usr,
            "songs_data": filtered_songs_data,
            "search_query": search_query,
            "showing_favorites": showing_favorites
        }
        return render_template("show_songs.html", **sust)
    return redirect(url_for("songs.show_songs"))

@song_bp.route("/toggle_favorite", methods=["POST"])
@flask_login.login_required
def toggle_favorite():
    usr = User.current_user()
    song_id = request.form.get("song_id")
    songs = list(srp.load_all(Song))

    if usr and song_id is not None:
        if song_id in usr.favorite_songs_ids:
            usr.remove_favorite_song(song_id)
            flask.flash("Canción desmarcada como favorita.")
        else:
            song = next((song for song in songs if song.id == song_id), None)
            if song:
                usr.add_favorite_song(song_id)
                flask.flash(f"{song.title} marcada como favorita.")
            else:
                flask.flash("Canción no encontrada.")
        
        srp.save(usr)
    else:
        flask.flash("Usuario no encontrado o ID de canción no proporcionado.")

    return flask.redirect(flask.url_for("songs.show_songs"))

@song_bp.route("/add_comment", methods=["POST"])
@flask_login.login_required
def add_comment():
    usr = User.current_user()
    song_id = request.form.get("song_id")
    comment_text = request.form.get("comment")

    if usr and song_id and comment_text:
        song = srp.find_first(Song, lambda s: s.id == song_id)
        if song:
            song.add_comment(usr.username, comment_text)
            srp.save(song)
            flask.flash("Comentario añadido correctamente.")
        else:
            flask.flash("Canción no encontrada.")
    else:
        flask.flash("Usuario no encontrado, ID de canción o comentario no proporcionado.")

    return flask.redirect(flask.url_for("songs.show_songs"))

@song_bp.route("/friend_songs/<friend_username>")
@flask_login.login_required
def friend_songs(friend_username):
    usr = User.current_user()
    friend = User.find_by_username(srp, friend_username)
    songs = list(srp.load_all(Song))

    if usr and friend:
        if friend.username in usr.friends:
            # Obtener los objetos Song asociados al amigo
            songs_data = [song for song in songs if song.id in friend._songs_oids]

            songs_data = []
            for song_oid in friend._songs_oids:
                song = srp.find_first(Song, lambda s: s.id == song_oid)
                if song:
                    song_dict = {
                        "id": song.id,
                        "title": song.title,
                        "artist": song.artist,
                        "genre": song.genre,
                        "comments": song.comments
                    }
                    songs_data.append(song_dict)
            print(songs_data)

            sust = {
                "usr": usr,
                "friend": friend,
                "songs_data": songs_data
            }
            return render_template("friend_songs.html", **sust)
        else:
            flask.flash("No tienes permiso para ver las canciones de este usuario.")
            return redirect(url_for("account.manage_friends"))
    else:
        flask.flash("Usuario o amigo no encontrado.")
        return redirect(url_for("account.manage_friends"))
