import flask
import flask_login
import sirope
import uuid

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
    usr = User.current_user()
    return flask.render_template("users.html", users=users, usr=usr)

@user_bp.route("/search", methods=["GET", "POST"])
@flask_login.login_required
def search_users():
    srp = sirope.Sirope()
    usr = User.current_user()

    if flask.request.method == "POST":
        search_query = flask.request.form.get("search_query")
        all_users = list(srp.load_all(User))
        users = [user for user in all_users if search_query.lower() in user.username.lower()]

        return flask.render_template("search_users.html", users=users, search_query=search_query, usr=usr)
    
    return flask.render_template("search_users.html" ,usr=usr)

@user_bp.route("/add_friend/<username>", methods=["POST"])
@flask_login.login_required
def add_friend(username):
    current_user = User.current_user()
    friend = srp.find_first(User, lambda u: u.username == username)

    if friend:
        existing_request = srp.find_first(FriendshipRequest, lambda fr: fr.sender == current_user.username and fr.receiver == friend.username)
        if existing_request:
            flask.flash("Ya has enviado una solicitud de amistad a este usuario.")
            print(f"Ya has enviado una solicitud de amistad a {friend.username}.")
        else:
            new_request = FriendshipRequest(id = str(uuid.uuid4()), sender=current_user.username, receiver=friend.username, status="pending")
            srp.save(new_request)
            flask.flash(f"Solicitud de amistad enviada a {friend.username}")

    return flask.redirect(flask.url_for("users.users"))