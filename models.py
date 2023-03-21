from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User (db.Model):
    """A user."""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        primary_key=True,
        unique=True,
    )

    password = db.Column(
        db.String(100),
        nullable=False,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )

    last_name = db.Column(
        db.String(30),
        nullable=False,
    )