import sirope
import flask_login
import werkzeug.security as safe

class User(flask_login.UserMixin):
    def __init__(self, email, username, password):
        self._email = email
        self._username = username
        self._password = safe.generate_password_hash(password)
        self._songs_oids = []
        self.friends = []
        self._friend_requests = []
        self.favorite_songs_ids  = []

    @property
    def email(self):
        return self._email
    
    @property
    def username(self):
        return self._username
    
    @property
    def oids_songs(self):
        if not self.__dict__.get("_songs_oids"):
            self._songs_oids = []
        return self._songs_oids

    def friend_requests(self):
        return self._friend_requests

    def get_id(self):
        return self.username
    
    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)

    def add_song_oid(self, song_oid):
        self.oids_songs.append(song_oid)
        
    def add_friend(self, friend_username):
        self.friends.append(friend_username)

    def add_friend_request(self, friend_request):
        self._friend_requests.append(friend_request)

    def add_favorite_song(self, song_id):
        if song_id not in self.favorite_songs_ids:
            self.favorite_songs_ids.append(song_id)

    def remove_favorite_song(self, song_id):
        if song_id in self.favorite_songs_ids:
            self.favorite_songs_ids.remove(song_id)

    @staticmethod
    def current_user():
        usr = flask_login.current_user

        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None

        return usr
    
    @staticmethod
    def find(s: sirope.Sirope, email: str) -> "User":
        return s.find_first(User, lambda u: u.email == email)
    
    @staticmethod
    def find_by_username(s: sirope.Sirope, username: str) -> "User":
        return s.find_first(User, lambda u: u.username == username)
