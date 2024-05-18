# /views/users/users_view.py

import flask
import flask_login
import sirope
from model.user import User

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
        users = list(srp.find(User, lambda u: search_query.lower() in u.username.lower()))
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
