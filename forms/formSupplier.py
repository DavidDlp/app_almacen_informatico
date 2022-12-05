from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length

class ModifiedFormSupplier(FlaskForm):
    company_name = StringField(validators=[InputRequired(), Length(max=50)]
                          , render_kw={"placeholder": "Enter you company name"})
    country = StringField(validators=[InputRequired(), Length(max=20)]
                          , render_kw={"placeholder": "Enter your country"})
    submit = SubmitField("Save Profile")