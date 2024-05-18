import sirope

class Song:
    def __init__(self, identificador, title, artist, genre):
        self._identificador = identificador
        self._title = title
        self._artist = artist
        self._genre = genre


    # @id.setter
    # def id(self, value):
    #     self._id = value

    @property
    def title(self):
        return self._title
    @property
    def identificador(self):
        return self._identificador
   
    @property
    def artist(self):
        return self._artist
    
    @property
    def genre(self):
        return self._genre

    @staticmethod
    def find(s: sirope.Sirope, title: str) -> "Song":
        return s.find_first(Song, lambda s: s.title == title)
