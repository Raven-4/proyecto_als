from app import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    artist = db.Column(db.String(128), index=True)
    genre = db.Column(db.String(64), index=True)
    # Agrega campos según sea necesario para el modelo de canción
