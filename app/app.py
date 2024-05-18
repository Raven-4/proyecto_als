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

    if not usr:
        return render_template("index.html", usr=usr)

    sust = {
        "usr": usr,
        "songs": songs
    }

    return render_template("show_songs.html", **sust)

@app.route("/add_song", methods=["POST"])
def add_song():
    if request.method == "POST":
        title = request.form.get("title")
        artist = request.form.get("artist")
        genre = request.form.get("genre")
        
        if not title:
            flask.flash("¿Y el título?")
            return flask.redirect(url_for("add_song"))
        
        if not artist:
            flask.flash("¿Y el artista?")
            return flask.redirect(url_for("add_song"))
        
        if not genre:
            flask.flash("¿Y el género?")
            return flask.redirect(url_for("add_song"))
        
        song = Song(title=title, artist=artist, genre=genre)
        srp.save(song)

        return flask.redirect(url_for("index"))
    
    return render_template("add_song.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            flask.flash("Email es requerido")
            return flask.redirect(url_for("register"))
        
        if not password:
            flask.flash("Contraseña es requerida")
            return flask.redirect(url_for("register"))

        existing_user = User.find(srp, email)
        if existing_user:
            flask.flash("Usuario ya registrado")
            return flask.redirect(url_for("register"))

        new_user = User(email, password)
        srp.save(new_user)

        flask.flash("Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
        return flask.redirect(url_for("index"))
    
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
