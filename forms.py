from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class RegisterUserForm(FlaskForm):
    """Form for user registration."""

    # TODO: Add Length validation for each field (since most have length limits)
    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )

    email = EmailField(
        "Email",
        validators=[InputRequired(), Email()]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired()]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired()]
    )


class LoginForm(FlaskForm):
    """Form to log users into the Flask Notes app."""

    # TODO: Optionally add length validators here, too.
    username = StringField(
        "Username",
        validators=[InputRequired()]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )


class EditNoteForm(FlaskForm):
    """Form to edit an existing note"""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)]
    )

    content = TextAreaField(
        "Content",
        validators=[InputRequired()]
    )


class AddNoteForm(FlaskForm):
    """Form to add new note"""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)]
    )

    content = TextAreaField(
        "Content",
        validators=[InputRequired()]
    )


class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""
