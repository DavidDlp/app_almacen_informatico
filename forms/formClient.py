from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length


class ModifiedFormClient(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(max=25)]
                       , render_kw={"placeholder": "Enter your name"})
    lastname = StringField(validators=[InputRequired(), Length(max=50)]
                           , render_kw={"placeholder": "Enter your lastname"})
    address = StringField(validators=[InputRequired(), Length(max=150)]
                       , render_kw={"placeholder": "Enter your address"})
    country = StringField(validators=[InputRequired(), Length(max=20)]
                       , render_kw={"placeholder": "Enter your country"})
    city = StringField(validators=[InputRequired(), Length(max=20)]
                          , render_kw={"placeholder": "Enter your city"})
    cp = IntegerField(validators=[InputRequired()]
                          , render_kw={"placeholder": "Enter your postal code"})
    phone = StringField(validators=[InputRequired(), Length(max=20)]
                       , render_kw={"placeholder": "Enter your phone"})
    submit = SubmitField("Save Profile")