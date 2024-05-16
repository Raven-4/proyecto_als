import json
import flask
import sirope
import flask_login
from flask import render_template, redirect, url_for, request
from models.song import Song
from models.user import User
# from models.forms import SongForm

def create_app():
    lmanager = flask_login.login_manager.LoginManager()
    fapp = flask.Flask(__name__)
    sirp = sirope.Sirope()

    fapp.config.from_file("instance/config.json", load=json.load)
    lmanager.init_app(fapp)
    return fapp, lmanager, sirp

app, lm, srp = create_app()

@lm.user_loader
def user_loader(email):
    return User.find(srp, email)

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")

@app.route('/')
def index():
    usr = User.current_user()
    songs = srp.load_all(Song)

    sust = {
        "usr": usr,
        "songs": songs
    }

    return render_template("index.html", **sust)

@app.route("/add_song", methods=["POST"])
def add_song():
    title = flask.request.form.get("title")
    artist = flask.request.form.get("artist")
    genre = flask.request.form.get("genre")
    
    if not title:
        flask.flash("¿Y el título?")
        return flask.redirect("/")
    
    if not artist:
        flask.flash("¿Y el artista?")
        return flask.redirect("/")
    
    if not genre:
        flask.flash("¿Y el género?")
        return flask.redirect("/")
    
    # Create a new Song instance (you need to define the Song class)
    song = Song(title=title, artist=artist, genre=genre)
    
    # Here you should save the song to your storage system (sirope)
    srp.save(song)

    # For now, let's print the details of the song
    print("New Song:")
    print("Title:", song.title)
    print("Artist:", song.artist)
    print("Genre:", song.genre)
    
    return flask.redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
