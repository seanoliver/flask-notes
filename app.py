from flask import Flask, redirect                                     # Import the Flask class
from flask_debugtoolbar import DebugToolbarExtension        # Import DebugToolbarExtension class
from models import connect_db, db                           # Import connect_db, db, and model
import os                                                   # Import os module for env vars & db link

app = Flask(__name__)                                       # Create Flask app instance
app.config['SECRET_KEY'] = "oh-so-secret"                   # Set app secret key
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False          # Disable Debug Toolbar redirect interception
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        # Disable SQL Alchemy track modifications
app.config['SQLALCHEMY_ECHO'] = True                        # Enable SQL Alchemy echo (print SQL statements)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(     # Set SQL Alchemy database URI
    "DATABASE_URL", "postgresql:///flask_notes")

debug = DebugToolbarExtension(app)                          # Initialize debug toolbar

connect_db(app)                                             # Connect database to the Flask app

@app.get('/')
def homepage():
    """Redirect to /register."""

    return redirect('/register')

# @app.route('/register', methods=['GET', 'POST'])
# def register_user():
