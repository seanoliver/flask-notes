# Import the Flask class
from flask import Flask, redirect, session, render_template, flash
# Import DebugToolbarExtension class
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Note
# Import connect_db, db, and model
from forms import RegisterUserForm, LoginForm, CSRFProtectForm, AddNoteForm, EditNoteForm
# Import os module for env vars & db link
import os

# TODO: Organize imports list:
#        - Start with os
#        - Sections for flask / external modules
#        - Sections for internal models, forms, etc.

# Create Flask app instance
app = Flask(__name__)
# Set app secret key
app.config['SECRET_KEY'] = "oh-so-secret"
# Disable Debug Toolbar redirect interception
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# Disable SQL Alchemy track modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Enable SQL Alchemy echo (print SQL statements)
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(     # Set SQL Alchemy database URI
    "DATABASE_URL", "postgresql:///flask_notes")

# Initialize debug toolbar
debug = DebugToolbarExtension(app)

# Connect database to the Flask app
connect_db(app)


@app.get('/')
def homepage():
    """Redirect to /register."""

    return redirect('/register')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user: produce form & handle form submission."""

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # TODO: Have a single register() function and pass user data into it
        user = User(
            username=username,
            password=User.get_password_hash(password),
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # TODO: db.session.add typically lives in the models.py
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        # on successful login, redirect to secret page
        flash("Registered!")
        return redirect(f"/users/{user.username}")

    else:

        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["username"] = user.username  # keep logged in
            flash("Logged in!")
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.get('/users/<username>')
def show_user_profile(username):
    """Renders the logged in user's page."""
    # TODO: Update docstring to reflect the if .. else behavior

    form = CSRFProtectForm()

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    elif session["username"] != username:
        # TODO: Could raise an UnauthorizedError to let them know they're not
        # allowed to go there.
        return redirect(f"/users/{session['username']}")
    else:
        user = User.query.get_or_404(username)
        notes = user.notes # TODO: Doing this here is an optional decision because you have access to notes in the user object

        return render_template(
            "profile.html",
            user=user,
            form=form,
            notes=notes
        )


@app.post('/logout')
def logout_user():
    """Log out the user and clear the username from the session object."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop("username", None)
    # TODO: Raise an UnauthorizedError in the event logout fails (e.g. they're
    # doing it from an incorrect source, etc.)
    return redirect("/")


@app.route('/users/<username>/notes/add', methods=["GET", "POST"])
def handle_add_note_form(username):
    """Adds note to user profile on form validation
    else renders template for errors"""

    form = AddNoteForm()

    # TODO: Need to prevent users from accessing other users' add notes page
    if "username" not in session:
        flash("You must be logged in to do this action!")
        return redirect("/")

    if username != session["username"]:
        flash("This is not your note.")
        return redirect(f'/users/{session["username"]}')


    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        note = Note(title=title, content=content, owner=username)

        db.session.add(note)
        db.session.commit()

        return redirect(f'/users/{username}')

    else:

        return render_template('add_note.html', form=form)


@app.route('/notes/<int:note_id>/update', methods=["GET", "POST"])
def handle_edit_note_form(note_id):
    """Display the form to edit a note and then once submitted, redirect
    the user to the user's profile page."""

    note = Note.query.get_or_404(note_id)

    if "username" not in session:
        flash("You must be logged in to do this action!")
        return redirect("/")

    if note.owner != session["username"]:
        flash("This is not your note.")
        return redirect(f'/users/{session["username"]}')

    form = EditNoteForm(obj=note)
    csrf_form = CSRFProtectForm() # Adding this for delete note button form

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f'/users/{note.owner}')

    else:

        return render_template(
            'edit_note.html',
            note=note,
            form=form,
            csrf_form=csrf_form
        )


@app.post('/users/<username>/delete')
def delete_user_account(username):
    """Delete user account and notes"""

    form = CSRFProtectForm()

    if form.validate_on_submit():

        # TODO: Move authentication checks up before validate on submit
        if "username" not in session:
            flash("You must be logged in to do this action!")
            return redirect("/")

        elif session["username"] != username:
            return redirect(f"/users/{session['username']}")

        else:
            flash("Account Successfully Deleted!") # TODO: Move this to after db.session.commit so we know user has been deleted

            user = User.query.get_or_404(username)
            notes = user.notes

            for note in notes:
                db.session.delete(note)

            db.session.delete(user)
            db.session.commit()

            session.pop("username", None)

            return redirect('/')

    else:

        return redirect('/')

@app.post('/notes/<int:note_id>/delete')
def delete_note(note_id):
    """Delete an individual note."""

    form = CSRFProtectForm()
    note = Note.query.get_or_404(note_id)

    if form.validate_on_submit():

        # TODO: Do authorization before getting the note and before form
        # validation.
        if "username" not in session:
            flash("You must be logged in to do this action!")
            return redirect("/")

        elif session["username"] != note.owner:
            flash("You can't delete that note!")
            return redirect(f"/users/{session['username']}")

        else:
            flash("Note Successfully Deleted!")

            db.session.delete(note)
            db.session.commit()

            return redirect(f"/users/{session['username']}")
    else:
        flash("Invalid Form Submission")
        return redirect('/')
