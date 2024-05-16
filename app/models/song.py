# from app import db

# class Song(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(128), index=True)
#     artist = db.Column(db.String(128), index=True)
#     genre = db.Column(db.String(64), index=True)
#     # Agrega campos según sea necesario para el modelo de canción

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
