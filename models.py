from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)

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

    @classmethod
    def get_password_hash(cls, password):
        """Return hashed password"""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        return hashed