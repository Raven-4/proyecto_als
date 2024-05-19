# /views/account/account_view.py

import flask
import flask_login
import sirope
from flask import render_template, redirect, url_for, request

from model.user import User
from model.friendshipRequest import FriendshipRequest

def get_account_blueprint():
    account = flask.Blueprint("account", __name__, url_prefix="/account", template_folder="templates", static_folder="static")
    srp = sirope.Sirope()
    return account, srp

account_bp, srp = get_account_blueprint()

@account_bp.route("/")
@flask_login.login_required
def account():
    return flask.render_template("account.html")

@account_bp.route("/change_password", methods=["GET", "POST"])
@flask_login.login_required
def change_password():
    if request.method == "POST":
        current_user = flask_login.current_user
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not current_password or not new_password or not confirm_password:
            flask.flash("Por favor, complete todos los campos.")
            return redirect(url_for("account.change_password"))

        if not current_user.chk_password(current_password):
            flask.flash("La contraseña actual no es correcta.")
            return redirect(url_for("account.change_password"))

        if new_password != confirm_password:
            flask.flash("Las contraseñas nuevas no coinciden.")
            return redirect(url_for("account.change_password"))

        current_user.set_password(new_password)
        srp.save(current_user)

        flask.flash("Contraseña cambiada exitosamente.")
        return redirect(url_for("account.account"))

    return render_template("change_password.html")

@account_bp.route("/manage_friends")
@flask_login.login_required
def manage_friends():
    current_user = User.current_user()
    if current_user:
        # Consulta las solicitudes de amistad donde el usuario actual es el receptor
        friend_requests = list(srp.load_all(FriendshipRequest))
        requests = [request for request in friend_requests if request.receiver == current_user.username and request.status == "pending"]
        friends = current_user.friends
        print(friends)

        return flask.render_template("friend_requests.html", friend_requests=requests, friends=friends)
    else:
        flask.flash("Debes iniciar sesión primero.")
        return flask.redirect(flask.url_for("index"))

@account_bp.route("/accept_friend_request", methods=["POST"])
@flask_login.login_required
def accept_friend_request():
    current_user = User.current_user()
    if current_user:
        request_id = flask.request.form.get("request_id")
        friend_request = srp.find_first(FriendshipRequest, lambda fr: fr.id == request_id)
        if friend_request:
            # Agregar al amigo a la lista de amigos del usuario actual
            current_user.add_friend(friend_request.sender)
            friend_request.accept()
            srp.save(current_user)
            srp.save(friend_request)
            print(friend_request.status)
            flask.flash(f"Solicitud de amistad de {friend_request.sender} aceptada.")
            return flask.redirect(flask.url_for("account.manage_friends"))
        else:
            flask.flash("Solicitud de amistad no encontrada.")
    else:
        flask.flash("Debes iniciar sesión primero.")
    return flask.redirect(flask.url_for("index"))

@account_bp.route("/reject_friend_request", methods=["POST"])
@flask_login.login_required
def reject_friend_request():
    current_user = User.current_user()
    if current_user:
        request_id = flask.request.form.get("request_id")
        friend_request = srp.find_first(FriendshipRequest, lambda fr: fr.id == request_id)
        if friend_request:
            # Eliminar la solicitud de amistad
            friend_request.reject()
            srp.save(friend_request)
            flask.flash(f"Solicitud de amistad de {friend_request.sender} rechazada.")
            return flask.redirect(flask.url_for("account.manage_friends"))
        else:
            flask.flash("Solicitud de amistad no encontrada.")
    else:
        flask.flash("Debes iniciar sesión primero.")
    return flask.redirect(flask.url_for("index"))
