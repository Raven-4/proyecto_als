import sirope

class Song:
    def __init__(self, id, title, artist, genre, comments=None):
        self._id = id
        self._title = title
        self._artist = artist
        self._genre = genre
        self.comments = comments if comments else []

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title
       
    @property
    def artist(self):
        return self._artist
    
    @property
    def genre(self):
        return self._genre

    def add_comment(self, user, comment):
        self.comments.append({"user": user, "comment": comment})

    def get_comments(self):
        return self.comments

    @staticmethod
    def find(s: sirope.Sirope, title: str) -> "Song":
        return s.find_first(Song, lambda s: s.title == title)
