from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from flask_login import UserMixin
from app.extensions import db

class Music(db.Model, UserMixin):
    __tablename__ = "musics"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    artist: Mapped[str] = mapped_column(String)
    image: Mapped[str] = mapped_column(String)
    song: Mapped[str] = mapped_column(String)

    def __init__(self, name, image, song, artist):
        self.name = name
        self.image = image
        self.song = song
        self.artist = artist