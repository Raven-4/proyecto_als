import sirope

class Song:
    def __init__(self, title, artist, genre):
        self._title = title
        self._artist = artist
        self._genre = genre

    @property
    def title(self):
        return self._title
    
    @property
    def artist(self):
        return self._artist
    
    @property
    def genre(self):
        return self._genre

    @staticmethod
    def find(s: sirope.Sirope, title: str) -> "Song":
        return s.find_first(Song, lambda s: s.title == title)
