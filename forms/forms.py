from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length, ValidationError
# models
from models.users import User


class RegisterFormUser(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "username"})

    password = PasswordField(validators=[InputRequired(), EqualTo('confirm'), Length(
        min=4, max=20)], render_kw={"placeholder": "password"})

    confirm = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "repita password"})

    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "Nombre"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(
            username=username.data
        ).first()

        if existing_username:
            raise ValidationError(
                "Este usuario ya existe. Por favor, elija otro diferente"
            )

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "password"})

    submit = SubmitField("Login")