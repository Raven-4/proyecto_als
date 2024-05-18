import json
import flask
import sirope
import flask_login
from flask import render_template, redirect, url_for, request
from models.song import Song
from models.user import User

def create_app():
    lmanager = flask_login.LoginManager()
    fapp = flask.Flask(__name__)
    sirp = sirope.Sirope()

    fapp.config.from_file("instance/config.json", load=json.load)
    lmanager.init_app(fapp)
    lmanager.login_view = 'index'  # Redirect to index if unauthorized
    return fapp, lmanager, sirp

app, lm, srp = create_app()

@lm.user_loader
def user_loader(username):
    return User.find_by_username(srp, username)

@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")

@app.route('/')
def index():
    usr = User.current_user()

    if not usr:
        return render_template("index.html", usr=usr)
    else:
        return redirect(url_for("show_songs"))

@app.route("/show_songs")
def show_songs():
    usr = User.current_user()
    songs = list(srp.load_all(Song))

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

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username:
        flask.flash("Nombre de Usuario es requerido")
        return flask.redirect(url_for("index"))

    if not password:
        flask.flash("Contraseña es requerida")
        return flask.redirect(url_for("index"))

    user = User.find_by_username(srp, username)

    if user and user.chk_password(password):
        flask_login.login_user(user)
        flask.flash("Inicio de sesión exitoso")
        return flask.redirect(url_for("show_songs"))
    else:
        flask.flash("Credenciales inválidas")
        return flask.redirect(url_for("index"))

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    flask.flash("Sesión cerrada exitosamente")
    return flask.redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        if not email:
            flask.flash("Email es requerido")
            return flask.redirect(url_for("register"))
        
        if not username:
            flask.flash("Nombre de Usuario es requerido")
            return flask.redirect(url_for("register"))

        if not password:
            flask.flash("Contraseña es requerida")
            return flask.redirect(url_for("register"))

        existing_user = User.find(srp, email)
        if existing_user:
            flask.flash("Email ya registrado")
            return flask.redirect(url_for("register"))

        existing_username = User.find_by_username(srp, username)
        if existing_username:
            flask.flash("Nombre de Usuario ya registrado")
            return flask.redirect(url_for("register"))

        new_user = User(email, username, password)
        srp.save(new_user)

        flask.flash("Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
        return flask.redirect(url_for("index"))
    
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
