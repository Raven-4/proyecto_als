# /views/users/users_view.py

import flask
import flask_login
import sirope

from model.user import User
from model.friendshipRequest import FriendshipRequest

def get_user_blueprint():
    user = flask.Blueprint("users", __name__, url_prefix="/users", template_folder="templates", static_folder="static")

    syrp = sirope.Sirope()
    return user, syrp

user_bp, srp = get_user_blueprint()

@user_bp.route("/")
@flask_login.login_required
def users():
    srp = sirope.Sirope()
    users = list(srp.load_all(User))
    return flask.render_template("users.html", users=users)

@user_bp.route("/search", methods=["GET", "POST"])
@flask_login.login_required
def search_users():
    srp = sirope.Sirope()
    if flask.request.method == "POST":
        search_query = flask.request.form.get("search_query")
        all_users = list(srp.load_all(User))
        users = [user for user in all_users if search_query.lower() in user.username.lower()]
        return flask.render_template("search_users.html", users=users, search_query=search_query)
    return flask.render_template("search_users.html")

@user_bp.route("/add_friend/<username>", methods=["POST"])
@flask_login.login_required
def add_friend(username):
    srp = sirope.Sirope()
    current_user = User.current_user()
    if current_user:
        friend = User.find_by_username(srp, username)
        if friend:
            current_user.add_friend(friend.username)
            srp.save(current_user)
            flask.flash(f"Friend request sent to {friend.username}")
    return flask.redirect(flask.url_for("users.users"))

@user_bp.route("/friend_requests")
@flask_login.login_required
def friend_requests():
    srp = sirope.Sirope()
    current_user = User.current_user()

    if current_user:
        friend_requests = current_user.friend_requests
        return flask.render_template("friend_requests.html", friend_requests=friend_requests)
    else:
        flask.flash("Debes iniciar sesión primero.")
        return flask.redirect(flask.url_for("index"))

@user_bp.route("/accept_friend_request/<int:request_id>", methods=["POST"])
@flask_login.login_required
def accept_friend_request(request_id):
    srp = sirope.Sirope()
    current_user = User.current_user()

    if current_user:
        friend_request = FriendshipRequest.query.get(request_id)
        if friend_request:
            current_user.accept_friend_request(friend_request)
            flask.flash(f"Solicitud de amistad de {friend_request.sender.username} aceptada.")
            return flask.redirect(flask.url_for("users.friend_requests"))
        else:
            flask.flash("Solicitud de amistad no encontrada.")
            return flask.redirect(flask.url_for("users.friend_requests"))
    else:
        flask.flash("Debes iniciar sesión primero.")
        return flask.redirect(flask.url_for("index"))


@user_bp.route("/reject_friend_request/<int:request_id>", methods=["POST"])
@flask_login.login_required
def reject_friend_request(request_id):
    srp = sirope.Sirope()
    current_user = User.current_user()

    if current_user:
        friend_request = FriendshipRequest.query.get(request_id)
        if friend_request:
            current_user.reject_friend_request(friend_request)
            flask.flash(f"Solicitud de amistad de {friend_request.sender.username} rechazada.")
            return flask.redirect(flask.url_for("users.friend_requests"))
        else:
            flask.flash("Solicitud de amistad no encontrada.")
            return flask.redirect(flask.url_for("users.friend_requests"))
    else:
        flask.flash("Debes iniciar sesión primero.")
        return flask.redirect(flask.url_for("index"))
