# /views/account/account_view.py

import flask
import flask_login
import sirope

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
    if flask.request.method == "POST":
        # Implementar el cambio de contraseña aquí
        flask.flash("Contraseña cambiada exitosamente.")
        return flask.redirect(flask.url_for("account.account"))
    return flask.render_template("change_password.html")

@account_bp.route("/manage_friends")
@flask_login.login_required
def manage_friends():
    current_user = User.current_user()
    if current_user:
        friend_requests = current_user.friend_requests
        return flask.render_template("friend_requests.html", friend_requests=friend_requests)
    else:
        flask.flash("Debes iniciar sesión primero.")
        return flask.redirect(flask.url_for("index"))

@account_bp.route("/accept_friend_request/<int:request_id>", methods=["POST"])
@flask_login.login_required
def accept_friend_request(request_id):
    current_user = User.current_user()
    if current_user:
        friend_request = FriendshipRequest.query.get(request_id)
        if friend_request:
            current_user.accept_friend_request(friend_request)
            flask.flash(f"Solicitud de amistad de {friend_request.sender.username} aceptada.")
            return flask.redirect(flask.url_for("account.manage_friends"))
        else:
            flask.flash("Solicitud de amistad no encontrada.")
            return flask.redirect(flask.url_for("account.manage_friends"))
    else:
        flask.flash("Debes iniciar sesión primero.")
        return flask.redirect(flask.url_for("index"))

@account_bp.route("/reject_friend_request/<int:request_id>", methods=["POST"])
@flask_login.login_required
def reject_friend_request(request_id):
    current_user = User.current_user()
    if current_user:
        friend_request = FriendshipRequest.query.get(request_id)
        if friend_request:
            current_user.reject_friend_request(friend_request)
            flask.flash(f"Solicitud de amistad de {friend_request.sender.username} rechazada.")
            return flask.redirect(flask.url_for("account.manage_friends"))
        else:
            flask.flash("Solicitud de amistad no encontrada.")
            return flask.redirect(flask.url_for("account.manage_friends"))
    else:
        flask.flash("Debes iniciar sesión primero.")
        return flask.redirect(flask.url_for("index"))
