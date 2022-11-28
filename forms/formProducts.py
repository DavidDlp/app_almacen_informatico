from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, TextAreaField
from wtforms.validators import InputRequired, Length


class RegisterFormProduct(FlaskForm):
    product_name = StringField(validators=[InputRequired(), Length(
        min=5, max=25)], render_kw={"placeholder": "product_name"})

    mark_product = StringField(validators=[InputRequired(), Length(max=25)], render_kw={"placeholder": "mark_product"})

    type_product = SelectField(choices=["Perifericos", "Portatiles", "Smartphones", "Monitores"], validators=[InputRequired()], render_kw={"placeholder": "type of product"})

    sale_price = DecimalField('Sale Price', places=2, validators=[InputRequired()], render_kw={"placeholder": "Sale price"})

    purchase_price = DecimalField('Purchase_price', places=2, validators=[InputRequired()], render_kw={"placeholder": "Purchase price"})

    description = TextAreaField('content', validators=[Length(min=10, max=255)])

    submit = SubmitField("Create New Product")