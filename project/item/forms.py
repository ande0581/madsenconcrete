# project/item/forms.py


from flask_wtf import Form
from wtforms import SelectField, FloatField
from wtforms.validators import DataRequired


class AddBidItemForm(Form):
    quantity = FloatField('quantity', validators=[DataRequired()])
    service_id = SelectField(
        'Item',
        coerce=int,
        validators=[DataRequired()],
        choices=[])