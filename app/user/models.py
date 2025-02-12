from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from flask_login import UserMixin
from app.extensions import db

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]

    def __init__(self, username, password):
        self.username = username
        self.password = password